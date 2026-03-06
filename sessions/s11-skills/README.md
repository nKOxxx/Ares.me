# Session 11: Skills

> **"Learn once, use everywhere"**

## What You Build

Modular capabilities that any agent can use.

## The Pattern

```
skills/
├── weather/
│   ├── SKILL.md        # Interface contract
│   ├── weather.py      # Implementation
│   └── test_weather.py # Tests
├── github/
│   ├── SKILL.md
│   └── github.py
└── notion/
    ├── SKILL.md
    └── notion.py
```

## SKILL.md Contract

```markdown
# Weather Skill

## Capabilities
- get_current(city: str) → Weather
- get_forecast(city: str, days: int) → List[Weather]

## Setup
- API key needed
- Rate limits apply

## Usage
```python
from skills.weather import WeatherSkill
weather = WeatherSkill(api_key)
temp = weather.get_current("London")
```
```

## Benefits

- **Reusable** — Any agent can use
- **Testable** — Skills have tests
- **Swappable** — Swap implementations
- **Documented** — Clear interface

## Next: Session 12

Production → [s12-production](../s12-production/)
