import argparse


def handle_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "config_file", type=str, required=True, help="The yaml file to load config from.")
    return parser.parse_args()
