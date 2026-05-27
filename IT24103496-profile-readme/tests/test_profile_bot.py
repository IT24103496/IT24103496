import importlib.util
import sys
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / ".github" / "scripts" / "profile_bot.py"
spec = importlib.util.spec_from_file_location("profile_bot", SCRIPT)
profile_bot = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = profile_bot
spec.loader.exec_module(profile_bot)


class ProfileBotTests(unittest.TestCase):
    def setUp(self):
        self.config = {
            "username": "IT24103496",
            "exclude_repositories": ["IT24103496"],
            "include_forks": True,
            "highlight_repositories": ["builtsmart"],
            "max_repositories": 4,
            "max_activity": 3,
        }
        self.repo = {
            "name": "builtsmart",
            "description": "Construction management system using Spring Boot and modern web technologies.",
            "html_url": "https://github.com/IT24103496/builtsmart",
            "language": "Java",
            "fork": True,
            "archived": False,
            "updated_at": "2026-05-01T00:00:00Z",
            "stargazers_count": 0,
        }

    def test_replace_block_changes_only_selected_module(self):
        original = "A\n<!-- LIVE_OVERVIEW_START -->\nold\n<!-- LIVE_OVERVIEW_END -->\nB"
        updated = profile_bot.replace_block(original, "LIVE_OVERVIEW", "new")
        self.assertIn("new", updated)
        self.assertTrue(updated.startswith("A"))
        self.assertTrue(updated.endswith("B"))

    def test_repository_filter_keeps_visible_forks_and_hides_profile_repo(self):
        repos = [self.repo, {**self.repo, "name": "IT24103496"}, {**self.repo, "name": "archived", "archived": True}]
        self.assertEqual(profile_bot.repo_filter(repos, self.config), [self.repo])

    def test_java_spring_repository_receives_priority_signal(self):
        generic = {**self.repo, "name": "notes", "description": "notes", "language": "HTML", "fork": False}
        self.assertGreater(profile_bot.repo_score(self.repo, ["builtsmart"]), profile_bot.repo_score(generic, []))

    def test_repo_table_labels_fork_and_java_badge(self):
        table = profile_bot.render_repos([self.repo], self.config)
        self.assertIn("builtsmart", table)
        self.assertIn("Forked public repository", table)
        self.assertIn("openjdk", table)

    def test_svg_metrics_returns_valid_profile_payload(self):
        svg = profile_bot.metrics_svg({"followers": 1}, [self.repo])
        self.assertIn("PUBLIC REPOS", svg)
        self.assertIn("JAVA REPOS", svg)
        self.assertIn("FOLLOWERS", svg)
        self.assertTrue(svg.startswith("<svg"))


if __name__ == "__main__":
    unittest.main()
