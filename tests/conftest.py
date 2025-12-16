from __future__ import annotations

import sys
from pathlib import Path


# When pytest is launched via the Windows console entrypoint (pytest.exe), Python
# sets sys.path[0] to the venv Scripts directory, not the project root.
# Adding the project root here ensures `import techlang` works consistently for:
# - `python -m pytest`
# - `pytest`
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
