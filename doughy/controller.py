from enum import Enum


class HeaterAction(Enum):
    ON = "on"
    OFF = "off"
    NO_CHANGE = "no_change"


class BangBangController:
    """Hysteresis (bang-bang) temperature controller.

    Heater turns ON when temp drops below (target - deadband),
    turns OFF when temp rises above (target + deadband),
    and does nothing in between.
    """

    def __init__(self, target_temp: float = 26.0, deadband: float = 0.5) -> None:
        self.target_temp = target_temp
        self.deadband = deadband
        self._heater_on = False

    def decide(self, current_temp: float) -> HeaterAction:
        """Pure decision function. No side effects beyond internal state."""
        if current_temp < self.target_temp - self.deadband:
            if not self._heater_on:
                self._heater_on = True
                return HeaterAction.ON
        elif current_temp > self.target_temp + self.deadband:
            if self._heater_on:
                self._heater_on = False
                return HeaterAction.OFF
        return HeaterAction.NO_CHANGE

    def update_target(self, new_target: float) -> None:
        self.target_temp = new_target
