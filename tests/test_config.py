import tempfile
from pathlib import Path

from doughy.config import DoughyConfig


class TestDoughyConfig:
    def test_defaults(self):
        c = DoughyConfig()
        assert c.target_temp == 26.0
        assert c.deadband == 0.5
        assert c.mock_hardware is False
        assert c.relay_pin == 17

    def test_load_from_yaml(self, tmp_path):
        cfg_file = tmp_path / "config.yaml"
        cfg_file.write_text("target_temp: 28.0\nmock_hardware: true\n")
        c = DoughyConfig.load(cfg_file)
        assert c.target_temp == 28.0
        assert c.mock_hardware is True
        # Other fields should be defaults
        assert c.deadband == 0.5

    def test_load_missing_file_returns_defaults(self, tmp_path):
        c = DoughyConfig.load(tmp_path / "nonexistent.yaml")
        assert c.target_temp == 26.0

    def test_load_ignores_unknown_keys(self, tmp_path):
        cfg_file = tmp_path / "config.yaml"
        cfg_file.write_text("target_temp: 24.0\nunknown_key: hello\n")
        c = DoughyConfig.load(cfg_file)
        assert c.target_temp == 24.0

    def test_load_empty_file(self, tmp_path):
        cfg_file = tmp_path / "config.yaml"
        cfg_file.write_text("")
        c = DoughyConfig.load(cfg_file)
        assert c.target_temp == 26.0
