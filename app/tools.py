import subprocess
import os
from typing import Dict, Any, List

class CodebaseSandbox:
    def __init__(self, repo_dir: str):
        self.repo_dir = os.path.abspath(repo_dir)

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
        full_path = os.path.join(self.repo_dir, relative_path)
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"File not found: {relative_path}")
        with open(full_path, "r", encoding="utf-8") as f:
            return f.read()

    def write_file(self, relative_path: str, content: str) -> str:
        """Overwrites content of a file in the repository."""
        full_path = os.path.join(self.repo_dir, relative_path)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Successfully updated {relative_path}"

    def run_tests(self) -> Dict[str, Any]:
        """Runs the pytest suite in the repo directory and returns structured pass/fail status and logs."""
        try:
            res = subprocess.run(
                ["pytest", "-v"],
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
