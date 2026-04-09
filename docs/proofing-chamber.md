# Proofing Chamber Build

A simple enclosed proofing chamber using an STC-1000 thermostat to hold fermentation temperature.

## Concept

An insulated enclosure with a heat source and temperature probe. The STC-1000 reads the probe and switches the heater on/off to maintain the target temperature. The dough container sits inside.

```
+---------------------------------------+
|  Insulated enclosure                  |
|                                       |
|   [Dough container]                   |
|                                       |
|                     [Temp probe]      |
|                                       |
|   [Heat source]                       |
+---------------------------------------+
        |
    STC-1000 relay
```

## Parts

| Item | Description | Est. Price |
|------|-------------|-----------|
| **STC-1000** | Thermostat controller with NTC probe | $8-15 |
| **Enclosure** | Styrofoam cooler box, small plastic storage tub, or modified cabinet. Bigger = more stable temp but slower to heat. A 30-50L cooler works well. | $5-20 |
| **Ceramic lamp holder** | E27 base, ceramic (not plastic — it sits in an enclosed warm space). | $2-3 |
| **Incandescent bulb** | 25-40W. Must be incandescent — LED bulbs produce almost no heat. | $1-2 |
| **Mains cable** | Short length of 2-core mains cable to wire the lamp holder to the STC-1000. | $2-5 |
| **Junction box** (recommended) | Small electrical enclosure to house the STC-1000 and mains connections with proper strain relief. | $3-5 |
| **12V PC fan** (optional) | 80mm or 120mm case fan for air circulation. Prevents hot spots near the heater. | $3-8 |
| **12V DC adapter** (for fan) | 1A is plenty. Standard barrel jack. | $3-5 |

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

### Bulb wiring detail

The ceramic lamp holder has two terminals (live and neutral). Wire them to the STC-1000 relay output and mains neutral:

```
                  STC-1000
                 +--------+
  Mains L ------>| 1      |
  Mains N ------>| 2    5 |----> Lamp holder L terminal
                 |      6 |----> Mains L (jumper from terminal 1)
                 |  7   8 |
                 +--|-----|+
                    |    |
                  NTC probe

  Mains N -----------------> Lamp holder N terminal
```

The STC-1000 relay (terminals 5-6) switches the live wire. Neutral goes straight from mains to the lamp holder.

All mains connections should be inside a junction box with strain relief on the cables. The lamp holder and cable then run from the junction box into the enclosure, with the bulb inside.

## Optional: 12V Fan

In a small enclosure, heat distributes well enough without a fan. If you notice uneven temperatures (e.g., with a large enclosure or a point heat source like a bulb), add a small 12V PC fan (80mm or 120mm) to circulate air. Wire it to a 12V adapter — red to (+), black to (-). The fan runs continuously and doesn't need to be switched by the STC-1000.

## Tips

- **Probe placement**: Put the probe near the dough, not touching the heater or walls. Clip it to the inside wall at dough height.
- **Insulation**: The better insulated, the less the heater cycles. Even lining a plastic tub with foil-backed foam board makes a big difference.
- **Bulb wattage**: Start with 25W in a small enclosure. 40W if it struggles to reach temperature. Too much wattage causes overshoot.
- **Ventilation**: You don't need air holes — sourdough fermentation doesn't consume enough oxygen to matter in a 30-50L enclosure. Opening the lid to check the dough is plenty.
