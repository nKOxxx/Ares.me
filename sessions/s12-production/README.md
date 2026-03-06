# Session 12: Production

> **"Real world, real impact"**

## What You Build

Deploy your agent to run 24/7.

## Deployment Options

### Option 1: Render (Recommended)
```yaml
# render.yaml
services:
  - type: web
    name: my-agent
    runtime: python
    plan: starter
    buildCommand: pip install -r requirements.txt
    startCommand: python agent.py
```

### Option 2: Vercel (Serverless)
```javascript
// api/agent.js
export default async function handler(req, res) {
  const response = await agent.process(req.body);
  res.json(response);
}
```

### Option 3: Self-Hosted
```bash
# Docker
docker build -t my-agent .
docker run -d my-agent
```

## Monitoring

```python
# Add to your agent
import logging

logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.FileHandler("agent.log"),
        logging.StreamHandler()
    ]
)

logger.info("Agent started")
logger.error("Task failed", exc_info=True)
```

## Health Checks

```python
@app.route("/health")
def health():
    return {
        "status": "healthy",
        "uptime": get_uptime(),
        "memory_usage": get_memory()
    }
```

## 🎉 You Did It!

You built an agent that:
- ✅ Uses tools effectively
- ✅ Remembers across sessions
- ✅ Has personality
- ✅ Acts proactively
- ✅ Collaborates securely
- ✅ Runs in production

**Now go build something that matters.**

---

<p align="center">
  <i>12 sessions complete ⚔️</i><br>
  <a href="../../">Back to Ares.me</a>
</p>
