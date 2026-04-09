import threading

from doughy.config import DoughyConfig
from doughy.controller import BangBangController
from doughy.db import TemperatureLog
from doughy.hardware.mock import MockRelay, MockSensor
from doughy.runner import DoughyRunner


class TestDoughyRunner:
    def test_runner_starts_and_stops(self, tmp_path):
        config = DoughyConfig(
            mock_hardware=True,
            read_interval_seconds=0.05,
            log_interval_seconds=0.0,
            db_path=str(tmp_path / "test.db"),
        )
        relay = MockRelay()
        sensor = MockSensor(relay, ambient=20.0)
        controller = BangBangController(target_temp=26.0, deadband=0.5)
        db = TemperatureLog(config.db_path)

        runner = DoughyRunner(config, sensor, relay, controller, db)

        # Run in a thread, stop after a short period
        t = threading.Thread(target=runner.run)
        t.start()
        threading.Event().wait(0.3)
        runner.stop()
        t.join(timeout=2.0)
        assert not t.is_alive()

        # Should have logged some readings
        db2 = TemperatureLog(config.db_path)
        rows = db2.recent(100)
        assert len(rows) > 0
        db2.close()

    def test_heater_off_on_shutdown(self, tmp_path):
        config = DoughyConfig(
            mock_hardware=True,
            read_interval_seconds=0.05,
            log_interval_seconds=100.0,
            db_path=str(tmp_path / "test.db"),
        )
        relay = MockRelay()
        sensor = MockSensor(relay, ambient=20.0)
        controller = BangBangController(target_temp=26.0, deadband=0.5)
        db = TemperatureLog(config.db_path)

        runner = DoughyRunner(config, sensor, relay, controller, db)

        t = threading.Thread(target=runner.run)
        t.start()
        threading.Event().wait(0.2)
        runner.stop()
        t.join(timeout=2.0)

        # Relay must be off after shutdown
        assert not relay.is_on()
