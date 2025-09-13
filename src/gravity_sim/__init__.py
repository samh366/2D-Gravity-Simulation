from gravity_sim.cli import handle_cli
from gravity_sim.simulation import Simulation


def main():
    args = handle_cli()
    runner = SimulationRunner(args.config)
    runner.run()
