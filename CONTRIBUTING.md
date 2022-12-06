# Contributing

## Requirements

- Python 3.7 or higher
- python3-virtualenv

## Set up a development environment

```bash
virtualenv -p python3 venv && \
  . venv/bin/activate && \
  pip install --requirement dev_requirements.txt
```

## Enable Git hooks

If you're planning to contribute code, it's a good idea to enable the standard Git hooks so that build scripts run before you commit. That way, you can see if basic tests pass in a few seconds rather than waiting a few minutes to watch them run in CircleCI.

```bash
./dev-scripts/hooks/enable_hooks
```
