import sys


def main() -> None:
    from py_plate.cows_and_bulls.core import run_game

    run_game()
    sys.exit()


if __name__ == "__main__":
    main()
