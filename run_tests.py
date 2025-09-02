import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Convenience entrypoint to run the test suite locally
exit_code = pytest.main([
    "tests",
    "-v",
    "--maxfail=1",
    "--disable-warnings"
])

sys.exit(exit_code)