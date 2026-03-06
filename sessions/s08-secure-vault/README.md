# Session 08: Secure Vault

> **"Trust without exposure"**

## What You Build

A secure credential-sharing system between agents.

## The Problem

```python
# BAD: Credentials in prompts
agent.run(f"Deploy to AWS with key {AWS_KEY}")  # Leaked to logs!

# BAD: Credentials in memory
agent.remember("api_key", "sk-...")  # Extractable
```

## The Solution: AgentVault Pattern

```python
# 1. Store credential securely
vault.store("aws_prod", credential, owner="agent1")

# 2. Share with specific agents
vault.share("aws_prod", to="agent2")

# 3. Agent retrieves at runtime
key = vault.retrieve("aws_prod")  # Decrypted only at use
```

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Agent 1   │────→│  AgentVault  │←────│   Agent 2   │
│  (Owner)    │     │  (Secure)    │     │ (Recipient) │
└─────────────┘     └──────────────┘     └─────────────┘
                            ↓
                    ┌──────────────┐
                    │   SQLite +   │
                    │   SQLCipher  │
                    └──────────────┘
```

## Security Layers

1. **Encryption at rest** — SQLCipher
2. **Access control** — Owner-granted permissions
3. **No memory leakage** — Retrieved only at execution
4. **Audit trail** — Who accessed what when

## Next: Session 09

Multi-agent collaboration → [s09-agentnet](../s09-agentnet/)
