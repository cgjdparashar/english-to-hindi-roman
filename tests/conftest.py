"""
Pytest configuration for unit tests
"""
import pytest
from pathlib import Path
import sys

# Add project root to Python path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Pytest markers
def pytest_configure(config):
    """Configure custom pytest markers"""
    config.addinivalue_line("markers", "slow: mark test as slow running")
    config.addinivalue_line("markers", "integration: integration test requiring external services")
    config.addinivalue_line("markers", "api: API endpoint tests")