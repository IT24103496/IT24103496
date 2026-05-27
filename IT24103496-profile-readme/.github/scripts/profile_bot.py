#!/usr/bin/env python3
"""Self-updating GitHub profile README bot using only public GitHub REST data."""
from __future__ import annotations

import html
import json
import os
import re
import urllib.error
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
README = ROOT / "README.md"
CONFIG = ROOT / "profile.config.json"
ASSETS = ROOT / "assets"
API_ROOT = "https://api.github.com"
COLORS = {
    "Java": "B07219",
    "HTML": "E34F26",
    "CSS": "1572B6",
    "JavaScript": "F7DF1E",
    "TypeScript": "3178C6",
    "Python": "3776AB",
    "Shell": "89E051",
    "C": "A8B9CC",
    "C++": "00599C",
}
LOGOS = {
    "Java": "openjdk",
    "HTML": "html5",
    "CSS": "css3",
    "JavaScript": "javascript",
    "TypeScript": "typescript",
    "Python": "python",
    "Shell": "gnubash",
    "C": "c",
    "C++": "cplusplus",
}


def load_config() -> dict[str, Any]:
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def request_json(path: str) -> Any:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "IT24103496-profile-bot",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.getenv("GITHUB_TOKEN", "").strip()
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(f"{API_ROOT}{path}", headers=headers)
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))


def markdown_escape(value: Any) -> str:
    return str(value or "").replace("|", "\\|").replace("\n", " ").strip()


def truncate(value: Any, limit: int = 118) -> str:
    text = " ".join(str(value or "").split())
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"


def replace_block(readme: str, marker: str, body: str) -> str:
    pattern = rf"<!-- {marker}_START -->.*?<!-- {marker}_END -->"
    replacement = f"<!-- {marker}_START -->\n{body.strip()}\n\n<!-- {marker}_END -->"
    updated, count = re.subn(pattern, replacement, readme, flags=re.DOTALL)
    if count != 1:
        raise ValueError(f"Expected exactly one marker block for {marker}; found {count}")
    return updated


def repo_filter(repos: list[dict[str, Any]], config: dict[str, Any]) -> list[dict[str, Any]]:
    excluded = set(config.get("exclude_repositories", []))
    allow_forks = bool(config.get("include_forks", False))
    return [
        repo for repo in repos
        if repo.get("name") not in excluded
        and not repo.get("archived")
        and (allow_forks or not repo.get("fork"))
    ]


def repo_score(repo: dict[str, Any], highlights: list[str]) -> float:
    score = 0.0
    if repo.get("name") in highlights:
        score += 24
    if repo.get("description"):
        score += 10
    score += min(int(repo.get("stargazers_count", 0)) * 3, 18)
    language = (repo.get("language") or "").lower()
    description = (repo.get("description") or "").lower()
    terms = ("spring", "java", "security", "network", "management", "rental", "backend", "api")
    if language == "java" or any(term in description for term in terms):
        score += 14
    if not repo.get("fork"):
        score += 8
    updated_at = repo.get("updated_at", "")
    if updated_at[:4].isdigit():
        days = (datetime.now(timezone.utc) - datetime.fromisoformat(updated_at.replace("Z", "+00:00"))).days
        if days <= 90:
            score += 10
        elif days <= 365:
            score += 5
    return score


def top_languages(repos: list[dict[str, Any]]) -> list[tuple[str, int]]:
    counts: Counter[str] = Counter(repo.get("language") for repo in repos if repo.get("language"))
    return counts.most_common(5)


def fmt_date(value: str) -> str:
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).strftime("%b %d, %Y")
    except ValueError:
        return "Recently"


def render_overview(profile: dict[str, Any], repos: list[dict[str, Any]], config: dict[str, Any]) -> str:
    languages = ", ".join(language for language, _ in top_languages(repos)) or "Projects incoming"
    followers = int(profile.get("followers", 0))
    forks = sum(1 for repo in repos if repo.get("fork"))
    return f'''## Live GitHub Pulse

<img src="./assets/live-metrics.svg" width="100%" alt="Live public GitHub profile metrics" />

| Signal | Current public data |
|---|---|
| Public repositories displayed | **{len(repos)}** |
| Forked repositories displayed | **{forks}** |
| Followers | **{followers}** |
| Primary repository languages | **{markdown_escape(languages)}** |

<sub>Generated from public GitHub API data by <code>profile-bot.yml</code>; commits occur only when displayed data changes.</sub>'''


def badge(language: str) -> str:
    color = COLORS.get(language, "475569")
    logo = LOGOS.get(language, "")
    logo_query = f"&logo={logo}&logoColor=white" if logo else ""
    return f"![{language}](https://img.shields.io/badge/{language.replace(' ', '%20')}-{color}?style=flat-square{logo_query})"


def render_repos(repos: list[dict[str, Any]], config: dict[str, Any]) -> str:
    if not repos:
        return "## Public Repositories\n\nFresh public projects will appear here automatically."
    highlights = config.get("highlight_repositories", [])
    ranked = sorted(repos, key=lambda repo: repo_score(repo, highlights), reverse=True)[: int(config.get("max_repositories", 6))]
    rows = ["## Public Repositories", "", "| Repository | Public signal |", "|---|---|"]
    for repo in ranked:
        name = markdown_escape(repo.get("name"))
        url = repo.get("html_url") or f"https://github.com/{config['username']}/{name}"
        description = markdown_escape(truncate(repo.get("description") or "Public repository."))
        language = repo.get("language") or "Code"
        origin = "Forked public repository" if repo.get("fork") else "Public repository"
        updated = fmt_date(repo.get("updated_at", ""))
        rows.append(
            f"| **[{name}]({url})**<br/><sub>{description}</sub> | {badge(language)}<br/><sub>{origin} · updated {updated}</sub> |"
        )
    return "\n".join(rows)


def event_line(event: dict[str, Any]) -> str | None:
    event_type = event.get("type", "")
    repo = event.get("repo", {}).get("name", "")
    if not repo:
        return None
    repo_url = f"https://github.com/{repo}"
    when = fmt_date(event.get("created_at", ""))
    if event_type == "PushEvent":
        count = len(event.get("payload", {}).get("commits", []))
        action = f"pushed {count} commit{'s' if count != 1 else ''} to"
    elif event_type == "CreateEvent":
        action = "created content in"
    elif event_type == "PullRequestEvent":
        action = "worked on a pull request in"
    elif event_type == "WatchEvent":
        action = "starred"
    elif event_type == "ForkEvent":
        action = "forked"
    else:
        return None
    return f"- **{when}** — {action} [{repo}]({repo_url})"


def render_activity(events: list[dict[str, Any]], config: dict[str, Any]) -> str:
    lines = [line for line in (event_line(event) for event in events) if line]
    lines = lines[: int(config.get("max_activity", 5))]
    if not lines:
        lines = ["- No recent supported public GitHub activity is visible yet."]
    return "## Recent Public Activity\n\n" + "\n".join(lines)


def metrics_svg(profile: dict[str, Any], repos: list[dict[str, Any]]) -> str:
    followers = int(profile.get("followers", 0))
    forks = sum(1 for repo in repos if repo.get("fork"))
    java_repos = sum(1 for repo in repos if repo.get("language") == "Java")
    values = [("PUBLIC REPOS", str(len(repos))), ("JAVA REPOS", str(java_repos)), ("FORKS SHOWN", str(forks)), ("FOLLOWERS", str(followers))]
    cards: list[str] = []
    x = 22
    for label, value in values:
        cards.append(f'<rect x="{x}" y="22" width="258" height="108" rx="18" fill="#06131F" stroke="#173446"/>')
        cards.append(f'<text x="{x+22}" y="58" fill="#94A3B8" font-family="JetBrains Mono, monospace" font-size="12" letter-spacing="1">{label}</text>')
        cards.append(f'<text x="{x+22}" y="101" fill="#F8FAFC" font-family="Inter, Arial" font-size="36" font-weight="800">{html.escape(value)}</text>')
        cards.append(f'<circle cx="{x+224}" cy="62" r="14" fill="#18E0D0" opacity=".18"/><circle cx="{x+224}" cy="62" r="6" fill="#A3E635"/>')
        x += 276
    return f'''<svg width="1130" height="152" viewBox="0 0 1130 152" xmlns="http://www.w3.org/2000/svg" role="img">
<defs><linearGradient id="bg" x2="1"><stop stop-color="#040B15"/><stop offset="1" stop-color="#111534"/></linearGradient></defs>
<rect width="1130" height="152" rx="22" fill="url(#bg)"/>{''.join(cards)}
</svg>\n'''


def main() -> int:
    config = load_config()
    username = config["username"]
    try:
        profile = request_json(f"/users/{username}")
        raw_repos = request_json(f"/users/{username}/repos?per_page=100&sort=updated&type=public")
        events = request_json(f"/users/{username}/events/public?per_page=30")
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        print(f"GitHub API unavailable; keeping existing live blocks: {exc}")
        return 0
    repos = repo_filter(raw_repos if isinstance(raw_repos, list) else [], config)
    readme = README.read_text(encoding="utf-8")
    readme = replace_block(readme, "LIVE_OVERVIEW", render_overview(profile, repos, config))
    readme = replace_block(readme, "PUBLIC_REPOS", render_repos(repos, config))
    readme = replace_block(readme, "ACTIVITY_FEED", render_activity(events if isinstance(events, list) else [], config))
    README.write_text(readme, encoding="utf-8")
    ASSETS.mkdir(exist_ok=True)
    (ASSETS / "live-metrics.svg").write_text(metrics_svg(profile, repos), encoding="utf-8")
    print(f"Updated live profile modules for {username}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
