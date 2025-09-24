from argparse import Namespace, ArgumentParser


def handle_cli() -> Namespace:
    """Return the command line arguments passed to the script.

    Returns:
        Namespace: Namespace containing the command line arguments.
    """
    parser = ArgumentParser()
    parser.add_argument("config_file", type=str, help="The yaml file to load config from.")
    return parser.parse_args()
