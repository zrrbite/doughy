import logging
import signal
import threading
import time

from .controller import BangBangController, HeaterAction
from .hardware.base import Relay, Sensor
from .config import DoughyConfig
from .db import TemperatureLog

logger = logging.getLogger("doughy")


class DoughyRunner:
    def __init__(
        self,
        config: DoughyConfig,
        sensor: Sensor,
        relay: Relay,
        controller: BangBangController,
        db: TemperatureLog,
    ) -> None:
        self.config = config
        self.sensor = sensor
        self.relay = relay
        self.controller = controller
        self.db = db
        self._stop = threading.Event()
        self._last_log_time = 0.0
        self.current_temp: float | None = None

    def run(self) -> None:
        """Main control loop. Blocks until stop() is called or SIGINT/SIGTERM."""
        logger.info(
            "Doughy starting. Target: %.1f°C, Deadband: ±%.1f°C",
            self.controller.target_temp,
            self.controller.deadband,
        )

        # Handle graceful shutdown (only from main thread)
        in_main_thread = threading.current_thread() is threading.main_thread()
        original_sigint = None
        if in_main_thread:
            original_sigint = signal.getsignal(signal.SIGINT)

            def _shutdown(signum, frame):
                logger.info("Shutdown signal received.")
                self.stop()

            signal.signal(signal.SIGINT, _shutdown)

        try:
            while not self._stop.wait(timeout=self.config.read_interval_seconds):
                self._tick()
        finally:
            self.relay.turn_off()
            self.db.close()
            if in_main_thread and original_sigint is not None:
                signal.signal(signal.SIGINT, original_sigint)
            logger.info("Doughy stopped. Heater OFF.")

    def _tick(self) -> None:
        temp = self.sensor.read_temperature_c()
        self.current_temp = temp

        action = self.controller.decide(temp)
        if action == HeaterAction.ON:
            self.relay.turn_on()
            logger.info("Heater ON  | %.2f°C (target %.1f°C)", temp, self.controller.target_temp)
        elif action == HeaterAction.OFF:
            self.relay.turn_off()
            logger.info("Heater OFF | %.2f°C (target %.1f°C)", temp, self.controller.target_temp)
        else:
            logger.debug(
                "%.2f°C | heater %s", temp, "ON" if self.relay.is_on() else "OFF"
            )

        now = time.monotonic()
        if now - self._last_log_time >= self.config.log_interval_seconds:
            self.db.record(temp, self.relay.is_on(), self.controller.target_temp)
            self._last_log_time = now

    def stop(self) -> None:
        self._stop.set()
