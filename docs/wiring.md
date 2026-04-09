# Wiring Guide

How to connect the DS18B20 temperature sensor and relay module to the Raspberry Pi 3.

## Raspberry Pi GPIO Pinout (relevant pins)

```
                    3.3V  (1) (2)  5V
                          (3) (4)  5V
                          (5) (6)  GND
  DS18B20 Data -> GPIO4   (7) (8)
                    GND   (9) (10)
  Relay IN   -> GPIO17   (11) (12)
                         (13) (14) GND
```

## DS18B20 Temperature Sensor

The DS18B20 uses the 1-Wire protocol on GPIO4 (the default 1-Wire pin on the Pi).

```
DS18B20 Probe (3 wires):
  Red    -> 3.3V (pin 1)
  Black  -> GND  (pin 6 or 9)
  Yellow -> GPIO4 (pin 7)

Pull-up resistor:
  4.7kΩ between Red (3.3V) and Yellow (data)
```

### Enable 1-Wire on the Pi

```bash
sudo raspi-config nonint do_onewire 0
```

Or manually add to `/boot/config.txt`:

```
dtoverlay=w1-gpio
```

Then reboot. The sensor should appear at `/sys/bus/w1/devices/28-*/w1_slave`.

## Relay Module

The relay switches the 12V heating mat on and off.

```
Relay module (3 pins, low-voltage side):
  VCC -> 5V  (pin 2)
  GND -> GND (pin 14)
  IN  -> GPIO17 (pin 11)

Relay screw terminals (high-voltage side):
  COM -> 12V PSU positive (+)
  NO  -> Heating mat positive (+)
  Heating mat negative (-) -> 12V PSU negative (-)
```

**NO = Normally Open**: the heating mat only gets power when the relay is energized (GPIO17 HIGH). This is the safe default — if the Pi crashes or loses power, the heater turns off.

## Wiring Diagram

```
                    +----------+
  3.3V (pin 1) ----|---+       |
                   |   |       |
                  4.7k |     DS18B20
                   |   |     probe
  GPIO4 (pin 7) ---|---+       |
                   |           |
  GND (pin 6) ----|---________/


                    +-----------+
  5V (pin 2)  -----|  VCC      |
  GND (pin 14) ----|  GND      |
  GPIO17 (pin 11) -|  IN       |
                   |    RELAY   |
                   |  COM  NO  |
                   +---|----|-  +
                       |    |
              12V PSU +     Heating mat +
              12V PSU - ----Heating mat -
```

## Configuration

The GPIO pin for the relay is configurable in `config.yaml`:

```yaml
relay_pin: 17            # BCM GPIO pin number
relay_active_high: true  # true = relay triggers on HIGH
```
