from pytest_mock import MockerFixture

from py_plate.__main__ import main


def test_main(mocker: MockerFixture) -> None:

    mock_run_game = mocker.patch("py_plate.cows_and_bulls.core.run_game")
    mock_exit = mocker.patch("py_plate.__main__.sys.exit")

    main()

    mock_run_game.assert_called_once()
    mock_exit.assert_called_once()
