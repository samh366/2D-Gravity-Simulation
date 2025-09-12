import argparse

def handle_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("hello")
    return parser.parse_args()