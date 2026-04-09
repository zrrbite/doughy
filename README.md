# Doughy

A Raspberry Pi 3 temperature controller for sourdough fermentation. Maintains a target temperature inside a food-safe container using a heating mat, DS18B20 temperature probe, and a relay — all off-the-shelf parts (~$30-55 excluding the Pi).

## How it works

A bang-bang (hysteresis) controller reads the temperature sensor every few seconds. When the temp drops below `target - deadband`, the heater turns on. When it rises above `target + deadband`, the heater turns off. Readings are logged to a SQLite database.

Typical sourdough bulk ferment: 24-28°C with a ±0.5°C deadband.

## Quick start

```bash
# Install
pip install -e .

# Copy and edit config (mock_hardware: true for PC development)
cp config.example.yaml config.yaml

# Run the controller
python -m doughy run

# Check recent readings
python -m doughy log

# Show latest reading
python -m doughy status

# Set a new target temperature
python -m doughy target 28.0
```

### On the Raspberry Pi

```bash
pip install -e ".[rpi]"
# Edit config.yaml: set mock_hardware to false
python -m doughy run
```

A systemd service file is included at `systemd/doughy.service` for running on boot.

## Mock hardware

The software runs on any PC (Windows/Mac/Linux) without GPIO hardware. Set `mock_hardware: true` in your config and it simulates realistic thermal dynamics — temperature rises when the heater is on, drifts toward ambient when off. Useful for development and testing.

## Docs

- [Shopping list](docs/shopping-list.md) — all parts needed with descriptions and prices
- [Wiring guide](docs/wiring.md) — GPIO pinout, DS18B20 and relay connections, wiring diagram

## Configuration

See [`config.example.yaml`](config.example.yaml) for all options. Key settings:

| Setting | Default | Description |
|---------|---------|-------------|
| `target_temp` | 26.0 | Target temperature in °C |
| `deadband` | 0.5 | Hysteresis band (±°C) |
| `mock_hardware` | false | Use simulated sensor/relay |
| `relay_pin` | 17 | BCM GPIO pin for relay |
| `read_interval_seconds` | 10 | Sensor polling interval |
| `log_interval_seconds` | 60 | Database logging interval |

## Tests

```bash
pip install -e ".[dev]"
pytest
```

All tests use mock hardware and run on any platform.
