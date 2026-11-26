from argparse import Namespace

import pytest
from pytest_mock import MockerFixture

from py_plate.cli import main, setup_argparse


def test_setup_argparse_defaults() -> None:
    args = setup_argparse().parse_args([])

    assert args.length == 5


@pytest.mark.parametrize("option", ["-l", "--length"])
def test_setup_argparse_accepts_length_option(option: str) -> None:
    args = setup_argparse().parse_args([option, "7"])

    assert args.length == 7


@pytest.mark.parametrize(
    "option, arg", [("invalid-option", "invalid-arg"), ("-l", "invalid-arg")]
)
def test_setup_argparse_rejects_invalid_option(option: str, arg: str) -> None:
    with pytest.raises(SystemExit):
        setup_argparse().parse_args([option, arg])


def test_main(mocker: MockerFixture) -> None:
    mock_setup_parser = mocker.patch("py_plate.cli.setup_argparse")
    mock_args = mock_setup_parser.return_value.parse_args
    mock_args.return_value = Namespace(length=1)
    mock_run_game = mocker.patch("py_plate.cli.run_game")

    main()

    mock_setup_parser.assert_called_once()
    mock_args.assert_called_once()
    mock_run_game.assert_called_once_with(1)
