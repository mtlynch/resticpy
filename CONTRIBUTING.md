# Contributing

## Requirements

- Python 3.7 or higher
- [uv](https://docs.astral.sh/uv/)

## Set up a development environment

```bash
uv venv --python python3.12 && \
  . .venv/bin/activate && \
  uv pip install --requirement dev_requirements.txt
```

## Enable Git hooks

If you're planning to contribute code, it's a good idea to enable the standard Git hooks so that build scripts run before you commit. That way, you can see if basic tests pass in a few seconds rather than waiting a few minutes to watch them run in CircleCI.

```bash
./dev-scripts/hooks/enable-hooks
```

## Proposing changes

- If you're making a small change, submit a PR to show your proposal.
- If you're making a large change (over 100 LOC or three hours of dev time), [file an issue](https://github.com/mtlynch/picoshare/issues/new/choose) first to talk through the proposed change. This prevents you from wasting time on a change that has a low chance of being accepted.

## Style

- resticpy follows the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html).

## How to get your PR merged quickly

- Read my guide, ["How to Make Your Code Reviewer Fall in Love with You,"](https://mtlynch.io/code-review-love/) to understand how to contribute effectively to an open source project.
- Give a clear, one-line title to your PR.
  - Good: `Fix dropped keystrokes on Firefox`
  - Bad: `Fix issue`
- If your PR is not ready for review, mark it as "draft."
- Merge or [rebase](https://www.atlassian.com/git/tutorials/rewriting-history/git-rebase) your changes with the latest `master` commit so that there are no merge conflicts.
- Your PR must pass build checks in CI before it will be considered for merge.
  - You'll see a green checkmark or red X next to your PR depending on whether your build passed or failed.
  - You are responsible for fixing formatting and tests to ensure that your code passes build checks in CI.

I try to review all PRs within three business days. If you've been waiting longer than this, feel free to comment on the PR to verify that it's on my radar.
