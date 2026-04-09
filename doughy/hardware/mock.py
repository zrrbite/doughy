import random
import time

from .base import Relay, Sensor


class MockRelay(Relay):
    def __init__(self) -> None:
        self._on = False

    def turn_on(self) -> None:
        self._on = True

    def turn_off(self) -> None:
        self._on = False

    def is_on(self) -> bool:
        return self._on


class MockSensor(Sensor):
    """Simulates thermal dynamics based on whether the relay (heater) is on."""

    def __init__(self, relay: MockRelay, ambient: float = 20.0) -> None:
        self._relay = relay
        self._temp = ambient
        self._ambient = ambient
        self._last_read = time.monotonic()

    def read_temperature_c(self) -> float:
        now = time.monotonic()
        dt = now - self._last_read
        self._last_read = now

        if self._relay.is_on():
            # Heater on: temp rises ~0.5°C/min, slowing as it approaches ceiling
            ceiling = self._ambient + 15.0
            self._temp += 0.5 * (dt / 60) * max(0, (ceiling - self._temp) / 15)
        else:
            # Heater off: temp drifts toward ambient ~0.2°C/min
            self._temp -= 0.2 * (dt / 60) * max(0, (self._temp - self._ambient) / 10)

        # Sensor noise
        self._temp += random.gauss(0, 0.05)
        return round(self._temp, 2)
