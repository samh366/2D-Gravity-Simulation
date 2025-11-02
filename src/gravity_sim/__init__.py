from gravity_sim.cli import handle_cli
from gravity_sim.simulation_runner import SimulationRunner


def main():
    """Run program."""
    args = handle_cli()
    SimulationRunner.run(args.config_file)
