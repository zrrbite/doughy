import sqlite3
from datetime import datetime, timezone


class TemperatureLog:
    def __init__(self, db_path: str = "doughy.db") -> None:
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._conn.execute("""
            CREATE TABLE IF NOT EXISTS readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                temperature_c REAL NOT NULL,
                heater_on INTEGER NOT NULL,
                target_temp REAL NOT NULL
            )
        """)
        self._conn.commit()

    def record(self, temp: float, heater_on: bool, target: float) -> None:
        self._conn.execute(
            "INSERT INTO readings (timestamp, temperature_c, heater_on, target_temp) "
            "VALUES (?, ?, ?, ?)",
            (datetime.now(timezone.utc).isoformat(), temp, int(heater_on), target),
        )
        self._conn.commit()

    def recent(self, n: int = 20) -> list[tuple]:
        cur = self._conn.execute(
            "SELECT timestamp, temperature_c, heater_on, target_temp "
            "FROM readings ORDER BY id DESC LIMIT ?",
            (n,),
        )
        return cur.fetchall()

    def close(self) -> None:
        self._conn.close()
