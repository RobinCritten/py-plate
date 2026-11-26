from argparse import ArgumentParser

from py_plate.cows_and_bulls.core import run_game


def setup_argparse() -> ArgumentParser:
    """Setup function for the `ArgumentParser` class

    Returns:
        ArgumentParser: Initialized and setup `ArgumentParser` instance
    """

    parser = ArgumentParser(
        prog="Py-Plate",
        description="Python project template with Cows and Bulls Demo",
        epilog="This CLI is for demonstrative purposes to be replaced or removed depending on project specification",
    )

    parser.add_argument("-l", "--length", default=5, type=int)

    return parser


def main() -> None:
    """Entry point for project CLI, reads args and runs the project"""
    parser = setup_argparse()
    args = parser.parse_args()
    run_game(args.length)
