import logging
from pathlib import Path

import click

from .config import DoughyConfig
from .controller import BangBangController
from .db import TemperatureLog
from .hardware import create_hardware
from .runner import DoughyRunner


@click.group()
@click.option(
    "--config",
    "-c",
    "config_path",
    default="config.yaml",
    type=click.Path(),
    help="Config file path.",
)
@click.pass_context
def cli(ctx, config_path):
    """Doughy — sourdough fermentation temperature controller."""
    ctx.ensure_object(dict)
    ctx.obj["config"] = DoughyConfig.load(Path(config_path))
    ctx.obj["config_path"] = Path(config_path)


@cli.command()
@click.option("-v", "--verbose", is_flag=True, help="Show debug-level output.")
@click.pass_context
def run(ctx, verbose):
    """Start the temperature controller."""
    config = ctx.obj["config"]
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
    )

    sensor, relay = create_hardware(config)
    controller = BangBangController(config.target_temp, config.deadband)
    db = TemperatureLog(config.db_path)

    runner = DoughyRunner(config, sensor, relay, controller, db)
    runner.run()


@cli.command()
@click.argument("temp", type=float)
@click.pass_context
def target(ctx, temp):
    """Set the target temperature (updates the config file)."""
    import yaml

    config_path = ctx.obj["config_path"]
    if config_path.exists():
        with open(config_path) as f:
            data = yaml.safe_load(f) or {}
    else:
        data = {}

    data["target_temp"] = temp
    with open(config_path, "w") as f:
        yaml.safe_dump(data, f, default_flow_style=False)

    click.echo(f"Target temperature set to {temp}°C")


@cli.command("log")
@click.option("-n", "--rows", default=20, help="Number of recent rows to show.")
@click.pass_context
def show_log(ctx, rows):
    """Show recent temperature readings."""
    config = ctx.obj["config"]
    db = TemperatureLog(config.db_path)
    readings = db.recent(rows)
    db.close()

    if not readings:
        click.echo("No readings yet.")
        return

    click.echo(f"{'Timestamp':<28} {'Temp (°C)':>10} {'Heater':>8} {'Target':>8}")
    click.echo("-" * 58)
    for ts, temp, heater, tgt in reversed(readings):
        ts_short = ts[:19].replace("T", " ")
        heater_str = "ON" if heater else "OFF"
        click.echo(f"{ts_short:<28} {temp:>9.2f} {heater_str:>8} {tgt:>7.1f}")


@cli.command()
@click.pass_context
def status(ctx):
    """Show the most recent reading."""
    config = ctx.obj["config"]
    db = TemperatureLog(config.db_path)
    readings = db.recent(1)
    db.close()

    if not readings:
        click.echo("No readings yet. Is the controller running?")
        return

    ts, temp, heater, tgt = readings[0]
    ts_short = ts[:19].replace("T", " ")
    heater_str = "ON" if heater else "OFF"
    click.echo(f"Time:    {ts_short}")
    click.echo(f"Temp:    {temp:.2f}°C")
    click.echo(f"Target:  {tgt:.1f}°C")
    click.echo(f"Heater:  {heater_str}")
