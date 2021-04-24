from pathlib import Path

import pytest


@pytest.fixture()
def test_data():
    return Path('dp_table/test_data.html').read_text()
