"""Exercise public CI in isolated Git repositories without private inputs."""
from pathlib import Path
import os
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class PublicCITests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.git("init", "-q")
        self.git("config", "user.email", "ci@example.invalid")
        self.git("config", "user.name", "CI test")
        (self.root / "scripts").mkdir()
        shutil.copyfile(ROOT / "scripts/ci.py", self.root / "scripts/ci.py")
        for name in ("progress.py", "ownership.py"):
            (self.root / "scripts" / name).write_text("raise SystemExit(0)\n")
        (self.root / ".gitignore").write_text(".analysis/\n*.exe\n__pycache__/\n")

    def git(self, *args):
        return subprocess.run(["git", *args], cwd=self.root, check=True,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def commit(self):
        self.git("add", ".")
        self.git("commit", "-qm", "fixture")

    def ci(self):
        return subprocess.run([sys.executable, "scripts/ci.py"], cwd=self.root,
                              env={**os.environ, "CI": "true", "PYTHONDONTWRITEBYTECODE": "1"},
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    def test_clean_checkout_and_ignored_local_outputs(self):
        (self.root / ".analysis").mkdir()
        (self.root / ".analysis/private.py").write_text("invalid syntax !")
        self.commit()
        self.assertEqual(self.git("status", "--porcelain").stdout, b"")
        result = self.ci()
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_bad_syntax_in_earlier_commit_is_checked(self):
        for suffix, source in (("py", "broken !"), ("json", "{"),
                               ("toml", "["), ("sh", "if then")):
            with self.subTest(suffix=suffix):
                path = self.root / ("broken." + suffix)
                path.write_text(source)
                self.commit()
                (self.root / "note.md").write_text("later unrelated commit " + suffix + "\n")
                self.commit()
                self.assertEqual(self.git("status", "--porcelain").stdout, b"")
                self.assertNotEqual(self.ci().returncode, 0)
                path.unlink()

    def test_force_added_private_artifact_is_rejected(self):
        (self.root / "original.exe").write_bytes(b"MZ")
        self.git("add", "-f", "original.exe")
        result = self.ci()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("original.exe", result.stderr)

    def test_ledger_checker_failure_is_propagated(self):
        for name in ("progress.py", "ownership.py"):
            with self.subTest(checker=name):
                path = self.root / "scripts" / name
                path.write_text("raise SystemExit(1)\n")
                self.assertNotEqual(self.ci().returncode, 0)
                path.write_text("raise SystemExit(0)\n")

    def test_staged_whitespace_is_checked(self):
        self.commit()
        (self.root / "note.md").write_text("trailing spaces  \n")
        self.git("add", "note.md")
        self.assertNotEqual(self.ci().returncode, 0)


if __name__ == "__main__":
    unittest.main()
