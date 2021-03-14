from pathlib import Path
from unittest.mock import patch

import pytest


@pytest.fixture(autouse=True, scope="function")
def config(tmpdir):
    class TestConfig:
        data = Path(tmpdir)

    config_instance = TestConfig()
    with patch("api.db.config") as m:
        m.Config.return_value = config_instance
        yield config_instance
