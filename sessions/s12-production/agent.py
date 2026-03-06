#!/usr/bin/env python3
"""
Session 12: Production
Deployment configurations and production best practices.
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime


class ProductionConfig:
    """
    Production configuration for agents.
    
    Handles:
    - Environment variables
    - Logging setup
    - Health checks
    - Graceful shutdown
    - Error handling
    """
    
    def __init__(self):
        self.env = os.getenv("AGENT_ENV", "development")
        self.debug = self.env == "development"
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.port = int(os.getenv("PORT", "8000"))
        
    def setup_logging(self):
        """Configure logging for production."""
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(logging.Formatter(log_format))
        
        # File handler (for production)
        if self.env == "production":
            Path("logs").mkdir(exist_ok=True)
            file_handler = logging.FileHandler(
                f"logs/agent-{datetime.now().strftime('%Y-%m-%d')}.log"
            )
            file_handler.setFormatter(logging.Formatter(log_format))
        
        # Root logger
        logging.basicConfig(
            level=getattr(logging, self.log_level),
            handlers=[console_handler] if self.debug else [console_handler, file_handler],
            format=log_format
        )
        
        return logging.getLogger(__name__)


class HealthChecker:
    """Health check endpoint for monitoring."""
    
    def __init__(self):
        self.checks: Dict[str, callable] = {}
        self.status = "healthy"
    
    def add_check(self, name: str, check_func):
        """Add a health check."""
        self.checks[name] = check_func
    
    def check(self) -> dict:
        """Run all health checks."""
        results = {}
        all_healthy = True
        
        for name, check_func in self.checks.items():
            try:
                result = check_func()
                results[name] = {"status": "healthy" if result else "unhealthy"}
                if not result:
                    all_healthy = False
            except Exception as e:
                results[name] = {"status": "error", "error": str(e)}
                all_healthy = False
        
        self.status = "healthy" if all_healthy else "unhealthy"
        
        return {
            "status": self.status,
            "timestamp": datetime.now().isoformat(),
            "checks": results
        }


class GracefulShutdown:
    """Handle graceful shutdown on signals."""
    
    def __init__(self):
        self.shutdown_handlers = []
        self.is_shutting_down = False
    
    def register_handler(self, handler):
        """Register a function to call on shutdown."""
        self.shutdown_handlers.append(handler)
    
    def shutdown(self, signal_num=None, frame=None):
        """Execute shutdown handlers."""
        if self.is_shutting_down:
            return
        
        self.is_shutting_down = True
        print("\n[SHUTDOWN] Initiating graceful shutdown...")
        
        for handler in self.shutdown_handlers:
            try:
                handler()
            except Exception as e:
                print(f"[SHUTDOWN] Error in handler: {e}")
        
        print("[SHUTDOWN] Complete. Exiting.")
        sys.exit(0)


def create_dockerfile():
    """Create a production Dockerfile."""
    dockerfile = '''# Production Dockerfile for Ares agent
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user for security
RUN useradd -m -u 1000 agentuser && chown -R agentuser:agentuser /app
USER agentuser

# Environment
ENV PYTHONUNBUFFERED=1
ENV AGENT_ENV=production

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \\
    CMD python -c "import sys; sys.exit(0)"

# Expose port
EXPOSE 8000

# Run
CMD ["python", "agent.py"]
'''
    
    Path("Dockerfile").write_text(dockerfile)
    print("✓ Created Dockerfile")


def create_render_yaml():
    """Create Render deployment config."""
    config = '''services:
  - type: web
    name: ares-agent
    runtime: python
    plan: starter
    buildCommand: pip install -r requirements.txt
    startCommand: python agent.py
    envVars:
      - key: AGENT_ENV
        value: production
      - key: LOG_LEVEL
        value: INFO
      - key: PYTHON_VERSION
        value: 3.11.0
    healthCheckPath: /health
    autoDeploy: true
'''
    
    Path("render.yaml").write_text(config)
    print("✓ Created render.yaml")


def create_docker_compose():
    """Create Docker Compose for local development."""
    compose = '''version: '3.8'

services:
  agent:
    build: .
    container_name: ares-agent
    environment:
      - AGENT_ENV=development
      - LOG_LEVEL=DEBUG
    volumes:
      - ./memory:/app/memory
      - ./logs:/app/logs
    ports:
      - "8000:8000"
    restart: unless-stopped
    
  agent-prod:
    build: .
    container_name: ares-agent-prod
    environment:
      - AGENT_ENV=production
      - LOG_LEVEL=INFO
    volumes:
      - agent-memory:/app/memory
      - agent-logs:/app/logs
    ports:
      - "8000:8000"
    restart: always
    profiles:
      - production

volumes:
  agent-memory:
  agent-logs:
'''
    
    Path("docker-compose.yml").write_text(compose)
    print("✓ Created docker-compose.yml")


def create_github_actions_deploy():
    """Create GitHub Actions workflow for deployment."""
    workflow = '''name: Deploy to Production

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest
      
      - name: Run tests
        run: pytest tests/ -v

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Deploy to Render
        env:
          RENDER_API_KEY: ${{ secrets.RENDER_API_KEY }}
        run: |
          # Deploy command would go here
          echo "Deploying to Render..."
      
      - name: Health check
        run: |
          sleep 30
          curl https://your-app.onrender.com/health || exit 1
'''
    
    workflow_dir = Path(".github/workflows")
    workflow_dir.mkdir(parents=True, exist_ok=True)
    (workflow_dir / "deploy.yml").write_text(workflow)
    print("✓ Created .github/workflows/deploy.yml")


def create_env_example():
    """Create example environment file."""
    env = '''# Ares Agent Environment Configuration

# Environment (development/production)
AGENT_ENV=development

# Logging (DEBUG, INFO, WARNING, ERROR)
LOG_LEVEL=INFO

# API Keys (set in production)
# OPENAI_API_KEY=sk-...
# ANTHROPIC_API_KEY=sk-ant-...

# Server settings
PORT=8000
HOST=0.0.0.0

# Memory settings
MEMORY_DIR=./memory
VAULT_KEY=your-encryption-key-here

# External services
# DATABASE_URL=postgresql://...
# REDIS_URL=redis://...
'''
    
    Path(".env.example").write_text(env)
    print("✓ Created .env.example")


def main():
    print("⚔️ Ares Session 12: Production")
    print("Deployment configurations and best practices.\n")
    
    # Create all deployment files
    create_dockerfile()
    create_render_yaml()
    create_docker_compose()
    create_github_actions_deploy()
    create_env_example()
    
    print("\n" + "="*50)
    print("Production setup complete!")
    print("\nNext steps:")
    print("1. Copy .env.example to .env and fill in your values")
    print("2. Test locally: docker-compose up")
    print("3. Deploy to Render: push to main branch")
    print("4. Set up monitoring and alerts")
    
    print("\nProduction checklist:")
    print("  ✓ Dockerfile for containerization")
    print("  ✓ render.yaml for cloud deployment")
    print("  ✓ docker-compose.yml for local dev")
    print("  ✓ GitHub Actions for CI/CD")
    print("  ✓ Environment configuration")
    print("  ✓ Health checks")
    print("  ✓ Logging setup")
    
    # Demo production config
    print("\n" + "="*50)
    print("Demo: Production configuration")
    
    config = ProductionConfig()
    logger = config.setup_logging()
    
    logger.info("Agent starting...")
    logger.info(f"Environment: {config.env}")
    logger.info(f"Debug mode: {config.debug}")
    logger.info(f"Port: {config.port}")
    
    # Demo health check
    health = HealthChecker()
    health.add_check("memory", lambda: True)
    health.add_check("api", lambda: True)
    
    status = health.check()
    logger.info(f"Health status: {status['status']}")
    
    print("\nProduction agent ready!")


if __name__ == "__main__":
    main()
