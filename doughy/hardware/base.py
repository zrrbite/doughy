from abc import ABC, abstractmethod


class SensorError(Exception):
    """Raised when a temperature sensor read fails."""


class Sensor(ABC):
    @abstractmethod
    def read_temperature_c(self) -> float:
        """Return current temperature in Celsius. Raise SensorError on failure."""
        ...


class Relay(ABC):
    @abstractmethod
    def turn_on(self) -> None:
        ...

    @abstractmethod
    def turn_off(self) -> None:
        ...

    @abstractmethod
    def is_on(self) -> bool:
        ...
