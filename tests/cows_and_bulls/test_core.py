from collections import Counter

import pytest

from py_plate.cows_and_bulls.core import Cows_And_Bulls


@pytest.fixture
def game():
    return Cows_And_Bulls()


def test_class_creation(game: Cows_And_Bulls) -> None:
    assert isinstance(game, Cows_And_Bulls)

    assert isinstance(game.goal_length, int)
    assert game.goal_length == 5

    assert isinstance(game.goal, str)
    assert len(game.goal) == game.goal_length

    assert isinstance(game.number_of_guesses, int)
    assert game.number_of_guesses == 0

    assert isinstance(game.goal_map, Counter)
    assert sum(game.goal_map.values()) == game.goal_length


def test_make_guess(game, mocker) -> None:
    mock_input = mocker.patch(
        "py_plate.cows_and_bulls.core.input", return_value="01234"
    )

    game.make_guess()

    assert game.current_guess == "01234"
    mock_input.assert_called_once()


def test_generate_goal(game, mocker):

    mock_randint = mocker.patch("py_plate.cows_and_bulls.core.randint", return_value=0)

    game.generate_goal()

    assert game.goal == "00000"
    mock_randint.assert_called_with(0, 9)
    assert mock_randint.call_count == game.goal_length


@pytest.mark.parametrize("guesses", ["01234", "00000", "99999"])
def test_validate_guess_valid_guesses(game, guesses):
    game.current_guess = guesses

    result: bool = game.validate_guess()

    assert result
    assert game.number_of_guesses == 1  # incremented on valid guess


@pytest.mark.parametrize(
    "guesses",
    ["1", "123", "123456", "1234567890", "a", "abc", "abcdef", "1a", "12345a"],
)
def test_validate_guess_incorrect_guess_length(game, mocker, guesses):
    game.current_guess = guesses

    mock_print = mocker.patch("py_plate.cows_and_bulls.core.print")

    result = game.validate_guess()

    assert not result
    assert game.number_of_guesses == 0
    mock_print.assert_called_once_with(
        f"Your guess was {len(game.current_guess)} digits long, please make sure your guess is the correct length ({game.goal_length})"
    )


@pytest.mark.parametrize(
    "guesses", ["abcde", "aaaaa", "!£$%^", "1234a", "a1234", "12a45"]
)
def test_validate_guess_incorrect_value(game, mocker, guesses):
    game.current_guess = guesses

    mock_print = mocker.patch("py_plate.cows_and_bulls.core.print")

    result = game.validate_guess()

    assert not result
    assert game.number_of_guesses == 0
    mock_print.assert_called_once_with(
        "Your guess contained non numeric values, please only use digits 0-9"
    )


def test_check_guess_correct_guess(game):
    game.goal = "00000"
    game.current_guess = "00000"
    result = game.check_guess()

    assert result


def test_check_guess_incorrect_guess(game, mocker):
    mock_bulls = mocker.patch.object(game, "bull_counter", return_value=1)
    mock_cows = mocker.patch.object(game, "cow_counter", return_value=2)
    mock_print = mocker.patch("py_plate.cows_and_bulls.core.print")

    game.current_guess = "00000"
    result = game.check_guess()

    assert not result
    mock_bulls.assert_called_once()
    mock_cows.assert_called_once_with(mock_bulls.return_value)
    mock_print.assert_called_once_with(
        f"The guess {game.current_guess} contains {mock_cows.return_value} cows and {mock_bulls.return_value} bulls"
    )


@pytest.mark.parametrize(
    "guess, goal, expected",
    [
        ("12345", "12345", 5),
        ("11111", "11111", 5),
        ("01111", "00000", 1),
        ("11110", "00000", 1),
        ("11011", "00000", 1),
        ("00111", "00000", 2),
        ("01110", "00000", 2),
        ("00000", "11111", 0),
    ],
)
def test_bull_counter(game, guess, goal, expected):
    game.current_guess = guess
    game.goal = goal
    result = game.bull_counter()

    assert result == expected


@pytest.mark.parametrize(
    "goal, guess, expected, bulls",
    [
        ("12345", "99999", 0, 0),
        ("12345", "12349", 0, 4),
        ("12345", "99991", 1, 0),
        ("12345", "11112", 1, 1),
    ],
)
def test_cow_counter(game, goal, guess, expected, bulls):
    game.current_guess = guess
    game.goal_map = Counter(goal)
    game.goal = goal
    result = game.cow_counter(bulls)

    assert result == expected


def test_play_retries_until_won(game, mocker):
    mocker.patch.object(game, "rules")
    mock_make_guess = mocker.patch.object(game, "make_guess")
    mock_validate_guess = mocker.patch.object(
        game, "validate_guess", side_effect=[False, True, True]
    )
    mock_check_guess = mocker.patch.object(
        game, "check_guess", side_effect=[False, True]
    )
    mock_print = mocker.patch("py_plate.cows_and_bulls.core.print")

    game.number_of_guesses = 2

    game.play()

    mock_make_guess.assert_called_once() if False else None
    assert mock_make_guess.call_count == 3
    assert mock_validate_guess.call_count == 3
    assert mock_check_guess.call_count == 2
    mock_print.assert_called_once_with(
        f"Congrats, you win! \n You guessed the correct answer in {game.number_of_guesses} guesses"
    )


def test_rules(game, mocker):
    mock_print = mocker.patch("py_plate.cows_and_bulls.core.print")

    game.rules()

    mock_print.assert_called_once()
