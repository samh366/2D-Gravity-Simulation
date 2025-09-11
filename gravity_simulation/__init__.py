import argparse

from gravity_simulation.cli import handle_cli

def main():
    args = handle_cli()
    print(args)