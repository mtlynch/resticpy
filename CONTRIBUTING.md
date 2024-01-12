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

Furthermore it's necessary to install node packages for utilities such as _prettier_:

```bash
npm install
```

## Testing

You can execute unit tests directly like this (just an example testcase):

```bash
python3 -m unittest ./restic/restic_test.py
```

or you can run the complete testsuite including coverage analysis using this script:

```bash
./dev-scripts/build
```

If you enabled GIT hooks this script will be executed with each commit.
Running it explicitly allows to go without GIT hooks though it should be executed before you push your code.
Obviously this script will be executed as part of the build pipeline to be safe.

## Formatting

Since the build pipeline checks for a strict format you should run the automated formatting before pushing your changes:

```bash
./dev-scripts/fix-style
```

## Enable Git hooks

If you're planning to contribute code, it's a good idea to enable the standard Git hooks so that build scripts run before you commit. That way, you can see if basic tests pass in a few seconds rather than waiting a few minutes to watch them run in CircleCI.

```bash
./dev-scripts/hooks/enable_hooks
```
