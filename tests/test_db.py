from doughy.db import TemperatureLog


class TestTemperatureLog:
    def test_record_and_recent(self, tmp_path):
        db = TemperatureLog(str(tmp_path / "test.db"))
        db.record(25.5, True, 26.0)
        db.record(26.1, True, 26.0)
        db.record(26.6, False, 26.0)

        rows = db.recent(10)
        assert len(rows) == 3
        # Most recent first
        assert rows[0][1] == 26.6
        assert rows[0][2] == 0  # heater off
        db.close()

    def test_recent_limit(self, tmp_path):
        db = TemperatureLog(str(tmp_path / "test.db"))
        for i in range(10):
            db.record(20.0 + i, False, 26.0)

        rows = db.recent(3)
        assert len(rows) == 3
        db.close()

    def test_empty_db(self, tmp_path):
        db = TemperatureLog(str(tmp_path / "test.db"))
        rows = db.recent()
        assert rows == []
        db.close()
