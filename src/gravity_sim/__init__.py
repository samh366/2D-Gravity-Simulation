from gravity_sim.cli import handle_cli
from gravity_sim.simulation import Simulation
from gravity_sim.config_loader import ConfigLoader


def main():
    args = handle_cli()
    sim = ConfigLoader.load_file(args.config)
    sim.run()
