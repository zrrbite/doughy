from __future__ import annotations

from typing import TYPE_CHECKING

from .base import Relay, Sensor

if TYPE_CHECKING:
    from doughy.config import DoughyConfig


def create_hardware(config: DoughyConfig) -> tuple[Sensor, Relay]:
    """Factory: returns (sensor, relay) pair — mock or real based on config."""
    if config.mock_hardware:
        from .mock import MockRelay, MockSensor

        relay = MockRelay()
        sensor = MockSensor(relay, ambient=config.mock_ambient_temp)
        return sensor, relay

    # Lazy imports — w1thermsensor/gpiozero only available on RPi
    from .ds18b20 import DS18B20Sensor
    from .relay import GPIORelay

    sensor = DS18B20Sensor()
    relay = GPIORelay(config.relay_pin, active_high=config.relay_active_high)
    return sensor, relay
