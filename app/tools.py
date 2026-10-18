import subprocess
import os
import sys
import tempfile
from pathlib import Path
from typing import Dict, Any, List

class CodebaseSandbox:
    def __init__(self, repo_dir: str):
        self.repo_dir = Path(repo_dir).resolve()
        if not self.repo_dir.is_dir():
            raise NotADirectoryError(f"Repository directory not found: {repo_dir}")

    def _resolve_file(self, relative_path: str) -> Path:
        """Resolve a repository-relative file without allowing path escapes."""
        candidate = Path(relative_path)
        if candidate.is_absolute():
            raise ValueError(f"Absolute paths are not allowed: {relative_path}")

        resolved = (self.repo_dir / candidate).resolve()
        try:
            resolved.relative_to(self.repo_dir)
        except ValueError as exc:
            raise ValueError(f"Path escapes repository: {relative_path}") from exc
        return resolved

    def list_files(self) -> List[str]:
        """Lists Python source and test files in the target repository."""
        files = []
        for root, _, filenames in os.walk(self.repo_dir):
            for f in filenames:
                if f.endswith(".py"):
                    rel_path = os.path.relpath(os.path.join(root, f), self.repo_dir)
                    files.append(rel_path)
        return files

    def read_file(self, relative_path: str) -> str:
        """Reads content of a file in the repository."""
        full_path = self._resolve_file(relative_path)
        if not full_path.is_file():
            raise FileNotFoundError(f"File not found: {relative_path}")
        with open(full_path, "r", encoding="utf-8") as f:
            return f.read()

    def write_file(self, relative_path: str, content: str) -> str:
        """Atomically replace an existing repository file."""
        full_path = self._resolve_file(relative_path)
        if not full_path.is_file():
            raise FileNotFoundError(f"File not found: {relative_path}")

        temp_path = None
        try:
            fd, temp_path = tempfile.mkstemp(
                dir=full_path.parent,
                prefix=f".{full_path.name}.",
                text=True,
            )
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                f.write(content)
                f.flush()
                os.fsync(f.fileno())
            os.replace(temp_path, full_path)
        finally:
            if temp_path and os.path.exists(temp_path):
                os.unlink(temp_path)
        return f"Successfully updated {relative_path}"

    def run_tests(self) -> Dict[str, Any]:
        """Runs the pytest suite in the repo directory and returns structured pass/fail status and logs."""
        try:
            res = subprocess.run(
                [sys.executable, "-m", "pytest", "-v"],
                cwd=self.repo_dir,
                capture_output=True,
                text=True,
                timeout=30
            )
            passed = (res.returncode == 0)
            return {
                "passed": passed,
                "exit_code": res.returncode,
                "stdout": res.stdout,
                "stderr": res.stderr
            }
        except subprocess.TimeoutExpired:
            return {
                "passed": False,
                "exit_code": -1,
                "stdout": "",
                "stderr": "Pytest execution timed out after 30 seconds."
            }
        except Exception as e:
            return {
                "passed": False,
                "exit_code": -1,
                "stdout": "",
                "stderr": str(e)
            }

    def get_diff(self) -> str:
        """Returns git diff if inside a git repository, or compares against backup."""
        res = subprocess.run(
            ["git", "diff"],
            cwd=self.repo_dir,
            capture_output=True,
            text=True
        )
        return res.stdout if res.stdout else "No git changes detected."
