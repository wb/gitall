from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
GITALL = PROJECT_ROOT / "gitall"


class GitAllIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        self.environment = os.environ.copy()
        self.environment.update(
            {
                "NO_COLOR": "1",
                "GIT_CONFIG_NOSYSTEM": "1",
                "GIT_CONFIG_GLOBAL": os.devnull,
            }
        )

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def git(self, repository: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", "-C", str(repository), *arguments],
            check=True,
            capture_output=True,
            text=True,
            env=self.environment,
        )

    def make_repository(self, name: str) -> Path:
        repository = self.root / name
        self.git(self.root, "init", "--quiet", str(repository))
        return repository

    def commit(self, repository: Path, message: str, date: str) -> str:
        environment = self.environment.copy()
        environment.update(
            {
                "GIT_AUTHOR_DATE": date,
                "GIT_COMMITTER_DATE": date,
            }
        )
        subprocess.run(
            [
                "git",
                "-C",
                str(repository),
                "-c",
                "user.name=GitAll Tests",
                "-c",
                "user.email=gitall@example.invalid",
                "commit",
                "--allow-empty",
                "--quiet",
                "-m",
                message,
            ],
            check=True,
            capture_output=True,
            text=True,
            env=environment,
        )
        return self.git(repository, "rev-parse", "HEAD").stdout.strip()

    def run_gitall(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(GITALL), *arguments],
            cwd=self.root,
            check=False,
            capture_output=True,
            text=True,
            env=self.environment,
        )

    def test_runs_repositories_in_name_order(self) -> None:
        self.make_repository("zeta")
        self.make_repository("alpha")

        result = self.run_gitall("status", "--short")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertLess(result.stdout.index("alpha"), result.stdout.index("zeta"))

    def test_preserves_raw_argument_boundaries_and_metacharacters(self) -> None:
        self.make_repository("repo")
        argument = "hello $USER; world"
        code = "import sys; print(repr(sys.argv[1:]))"

        result = self.run_gitall("--raw", sys.executable, "-c", code, argument)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(repr([argument]), result.stdout)

    def test_preserves_git_argument_boundaries_and_metacharacters(self) -> None:
        repository = self.make_repository("repo")
        value = "hello $USER; world"

        result = self.run_gitall("config", "gitall.test-value", value)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            self.git(repository, "config", "--get", "gitall.test-value").stdout.strip(),
            value,
        )

    def test_reports_failure_and_returns_nonzero_after_processing_all(self) -> None:
        self.make_repository("alpha")
        self.make_repository("beta")
        code = (
            "import os,sys; "
            "sys.exit(7 if os.path.basename(os.getcwd()) == 'alpha' else 0)"
        )

        result = self.run_gitall("--raw", sys.executable, "-c", code)

        self.assertEqual(result.returncode, 1)
        self.assertIn("alpha: exit 7", result.stderr)
        self.assertIn("beta", result.stdout)

    def test_include_and_exclude_select_repositories(self) -> None:
        self.make_repository("alpha")
        self.make_repository("beta")
        self.make_repository("gamma")

        result = self.run_gitall(
            "--include", "beta,alpha", "--exclude", "beta", "status", "--short"
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("alpha", result.stdout)
        self.assertNotIn("beta", result.stdout)
        self.assertNotIn("gamma", result.stdout)

    def test_include_file_adds_repositories(self) -> None:
        self.make_repository("alpha")
        self.make_repository("beta")
        include_file = self.root / "repositories.txt"
        include_file.write_text("beta\nalpha\n", encoding="utf-8")

        result = self.run_gitall(
            "--include-from", str(include_file), "status", "--short"
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertLess(result.stdout.index("alpha"), result.stdout.index("beta"))

    def test_repository_aliases_run_only_once(self) -> None:
        self.make_repository("repo")
        code = "print('command-executed')"

        result = self.run_gitall(
            "--include", "repo,./repo", "--raw", sys.executable, "-c", code
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.count("command-executed"), 1)

    def test_detects_linked_worktrees(self) -> None:
        repository = self.make_repository("primary")
        self.commit(repository, "initial", "2020-01-01T12:00:00+00:00")
        self.git(repository, "branch", "linked-branch")
        linked = self.root / "linked"
        self.git(repository, "worktree", "add", "--quiet", str(linked), "linked-branch")

        result = self.run_gitall("status", "--short")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("linked", result.stdout)
        self.assertIn("primary", result.stdout)

    def test_date_checkout_supports_punctuated_branch_names(self) -> None:
        repository = self.make_repository("repo")
        first_commit = self.commit(
            repository, "first", "2020-01-01T12:00:00+00:00"
        )
        self.commit(repository, "second", "2020-01-03T12:00:00+00:00")
        self.git(repository, "branch", "feature/example-1")

        result = self.run_gitall(
            "--date", "2020-01-02", "checkout", "feature/example-1"
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            self.git(repository, "rev-parse", "HEAD").stdout.strip(), first_commit
        )

    def test_date_checkout_reports_when_no_commit_matches(self) -> None:
        repository = self.make_repository("repo")
        self.commit(repository, "initial", "2020-01-02T12:00:00+00:00")

        result = self.run_gitall("--date", "2019-01-01", "checkout", "HEAD")

        self.assertEqual(result.returncode, 1)
        self.assertIn("no commit found", result.stderr)

    def test_explicit_non_repository_is_reported(self) -> None:
        (self.root / "not-a-repository").mkdir()

        result = self.run_gitall("--include", "not-a-repository", "status")

        self.assertEqual(result.returncode, 1)
        self.assertIn("not a Git repository", result.stderr)

    def test_rejects_parent_repository_path(self) -> None:
        result = self.run_gitall("--include", "../outside", "status")

        self.assertEqual(result.returncode, 2)
        self.assertIn("must stay beneath", result.stderr)

    def test_rejects_absolute_repository_path(self) -> None:
        result = self.run_gitall("--include", str(self.root), "status")

        self.assertEqual(result.returncode, 2)
        self.assertIn("must stay beneath", result.stderr)

    def test_launch_error_does_not_abort_remaining_repositories(self) -> None:
        self.make_repository("alpha")
        self.make_repository("beta")
        command = self.root / "not-executable"
        command.write_text("not executable\n", encoding="utf-8")
        command.chmod(0o644)

        result = self.run_gitall("--raw", str(command))

        self.assertEqual(result.returncode, 1)
        self.assertIn("alpha: exit", result.stderr)
        self.assertIn("beta: exit", result.stderr)

    def test_case_collisions_have_total_order(self) -> None:
        self.make_repository("Alpha")
        if (self.root / "alpha").exists():
            self.skipTest("filesystem is case-insensitive")
        self.make_repository("alpha")

        result = self.run_gitall("status", "--short")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertLess(result.stdout.index("Alpha"), result.stdout.index("alpha"))

    def test_repeated_verbose_adds_repository_path(self) -> None:
        repository = self.make_repository("repo")

        result = self.run_gitall("-vv", "status", "--short")

        self.assertEqual(result.returncode, 0, result.stderr)
        verbose_labels = [
            line
            for line in result.stdout.splitlines()
            if line.startswith("repo (") and line.endswith(")")
        ]
        self.assertEqual(len(verbose_labels), 1)
        reported_path = Path(verbose_labels[0][len("repo (") : -1])
        self.assertTrue(reported_path.is_absolute())
        self.assertTrue(reported_path.samefile(repository))

    def test_repeated_quiet_suppresses_gitall_output(self) -> None:
        self.make_repository("repo")

        result = self.run_gitall("-qq", "status", "--short")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "")


if __name__ == "__main__":
    unittest.main()
