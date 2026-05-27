# Automation design

## Included workflows

| Workflow | Purpose | Write access |
|---|---|---|
| `profile-bot.yml` | Refreshes public-data README blocks and local SVG metrics daily or on demand. | `contents: write` only, for generated visible changes. |
| `quality-gate.yml` | Runs tests, compiles scripts and validates README/assets on pushes and pull requests. | Read-only. |
| `snake.yml` | Produces light and dark contribution-trail SVGs in the `output` branch. | `contents: write` only. |
| `codeql.yml` | Runs GitHub CodeQL analysis of the Python bot code. | `security-events: write` for results. |

## Profile Bot logic

`profile_bot.py` fetches public user, repository and event data through GitHub's REST API. It includes visible forks because Dasun's currently visible portfolio repositories are forks, labels them honestly, prioritizes repositories configured as highlights, and updates only the three protected README blocks.

The bot generates `assets/live-metrics.svg` in-repository rather than using an external statistics-card service for the primary dashboard. Because timestamps are not embedded in generated output, scheduled runs commit only when visible public data or configured design changes.

## Security and maintenance choices

The Python bot has no third-party Python dependencies. GitHub Actions dependencies are monitored by Dependabot, the quality workflow validates SVG XML and README markers, and CodeQL scans the automation source.
