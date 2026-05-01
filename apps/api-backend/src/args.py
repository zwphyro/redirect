from argparse import ArgumentParser


def get_args():
    argument_parser = ArgumentParser()
    argument_parser.add_argument(
        "--dev",
        action="store_true",
        help="Run in development mode",
    )
    return argument_parser.parse_args()
