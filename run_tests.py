import sys
import os
import pytest

# Add current directory to sys.path so techlang can be imported
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Run all tests in the 'tests' folder with verbose output
exit_code = pytest.main([
    "tests",          # folder to search for tests
    "-v",             # verbose output
    "--maxfail=1",    # stop after first failure (optional)
    "--disable-warnings"  # hide warnings for clarity
])

# Exit with the pytest exit code
sys.exit(exit_code)