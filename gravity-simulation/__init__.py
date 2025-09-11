import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("hello")
    args = parser.parse_args()
    print(args)