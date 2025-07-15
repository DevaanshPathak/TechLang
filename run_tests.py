import sys
import os
import pytest

# Add current dir to sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

pytest.main(["tests"])
