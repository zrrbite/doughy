# Proofing Chamber Build

A simple enclosed proofing chamber using an STC-1000 thermostat to hold fermentation temperature.

## Concept

An insulated enclosure with a heat source, temperature probe, and a small fan for air circulation. The STC-1000 reads the probe and switches the heater on/off to maintain the target temperature. The dough container sits inside.

```
+---------------------------------------+
|  Insulated enclosure                  |
|                                       |
|   [Dough container]                   |
|                                       |
|   [Dish of water]   [Temp probe]      |
|                                       |
|   [Heat source]     [12V fan]         |
+---------------------------------------+
        |                  |
    STC-1000 relay     12V adapter
```

## Parts

| Item | Description | Est. Price |
|------|-------------|-----------|
| **STC-1000** | Thermostat controller with NTC probe | $8-15 |
| **Enclosure** | Styrofoam cooler box, small plastic storage tub, or modified cabinet. Bigger = more stable temp but slower to heat. A 30-50L cooler works well. | $5-20 |
| **Heat source** | Incandescent bulb (25-40W) with ceramic socket, or a reptile heat mat. Incandescent bulbs are cheap and produce gentle, even heat. | $3-10 |
| **12V PC fan** (optional) | 80mm or 120mm case fan for air circulation. Prevents hot spots near the heater. | $3-8 |
| **12V DC adapter** (for fan) | 1A is plenty. Standard barrel jack. | $3-5 |
| **Dish of water** | Keeps humidity up so the dough surface doesn't dry out. | free |

## STC-1000 Wiring

The STC-1000 has screw terminals on the back. It switches mains power to the heat source.

**Important: mains wiring is dangerous. If you're not comfortable with it, use an Inkbird ITC-308 instead — it's plug-and-play.**

```
Mains in (live + neutral):
  Live (L)    -> STC-1000 terminal 1
  Neutral (N) -> STC-1000 terminal 2

Heating output:
  STC-1000 terminal 5 (relay COM)  -> Heat source live
  STC-1000 terminal 6 (relay NO)   -> Mains live (L)
  Heat source neutral              -> Mains neutral (N)

Probe:
  NTC probe wires -> STC-1000 terminals 7 and 8 (no polarity)
```

The relay is wired in series with the live wire to the heat source. When the temperature drops below the setpoint, the relay closes and the heater gets power.

## 12V Fan Hookup

The fan runs continuously to circulate air — it doesn't need to be switched by the STC-1000.

### Option A: USB fan (simplest)

Use a USB-powered fan and plug it into any USB charger. No wiring needed.

### Option B: 12V PC fan with adapter

A standard PC case fan (80mm or 120mm) runs on 12V DC.

```
12V DC adapter:
  (+) positive -> Fan red wire
  (-) negative -> Fan black wire
```

Most 12V adapters have a barrel jack. You can either:
- Cut the barrel jack off and wire directly to the fan leads
- Use a barrel jack breakout board (~$1) for screw terminals

If the fan has a 3-pin or 4-pin PC connector, cut it off and use the red (+12V) and black (GND) wires. Ignore the yellow (tach) and blue (PWM) wires if present.

### Option C: Share the STC-1000 power supply

If your heat source is also 12V (e.g., a reptile heat mat on a 12V adapter), you can power the fan from the same 12V supply — just wire the fan in parallel. The fan draws very little current (<0.2A).

```
12V adapter (+) ---+--- Heat mat (+)
                   +--- Fan red wire

12V adapter (-) ---+--- Heat mat (-)
                   +--- Fan black wire
```

In this setup, the STC-1000 relay switches the heat mat but the fan runs continuously.

## Tips

- **Probe placement**: Put the probe near the dough, not touching the heater or walls. Clip it to the inside wall at dough height.
- **Insulation**: The better insulated, the less the heater cycles. Even lining a plastic tub with foil-backed foam board makes a big difference.
- **Humidity**: A small open dish of warm water inside prevents the dough surface from drying out during long ferments.
- **Bulb wattage**: Start with 25W in a small enclosure. 40W if it struggles to reach temperature. Too much wattage causes overshoot.
- **Ventilation**: You don't need air holes — sourdough fermentation doesn't consume enough oxygen to matter in a 30-50L enclosure. Opening the lid to check the dough is plenty.
