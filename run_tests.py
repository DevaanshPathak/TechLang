import sys
import os
import pytest
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Convenience entrypoint to run the test suite locally
exit_code = pytest.main([
    "tests",
    "-v",
    "--maxfail=1",
    "--disable-warnings"
])

# Clean up test artifacts if tests passed
if exit_code == 0:
    artifacts = [
        Path("techlang.db"),
        Path("techlang_canvas.png")
    ]
    for artifact in artifacts:
        if artifact.exists():
            try:
                artifact.unlink()
                print(f"[Cleanup] Removed test artifact: {artifact}")
            except Exception as e:
                print(f"[Warning] Could not remove {artifact}: {e}")

sys.exit(exit_code)