"""
Unit tests for Synapse AI - Storage & user persistence helper.
"""

import os
from utils.storage_helper import get_user_file_path, ensure_data_dir

def test_ensure_data_dir():
    ensure_data_dir()
    path = get_user_file_path("test_user_123")
    assert path.endswith("test_user_123.json")
    assert os.path.exists(os.path.dirname(path))
