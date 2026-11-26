from collections import Counter
from random import randint


class Cows_And_Bulls:
    goal_length: int
    goal: str
    goal_map: dict[str, int]

    number_of_guesses: int = 0
    current_guess: str

    def __init__(self, goal_length: int = 5):
        """Initialization function for Cows_And_Bulls class

        Args:
            goal_length (int, optional): Sets the length of the goal to be guessed. Defaults to 5.
        """
        self.goal_length = goal_length
        self.generate_goal()
        self.goal_map = Counter(self.goal)

    def generate_goal(self) -> None:
        """generates the goal of the game to be guessed and stores the result to `self.goal`"""

        digit_collection: str = ""

        for _ in range(self.goal_length):
            digit_collection += str(randint(0, 9))

        self.goal = digit_collection

    def validate_guess(self) -> bool:
        """Validates if `self.current_guess` is a valid input containing only numerical digits and is the correct length

        Returns:
            bool: status of validation
        """

        if len(self.current_guess) != self.goal_length:
            print(
                f"Your guess was {len(self.current_guess)} digits long, please make sure your guess is the correct length ({self.goal_length})"
            )
            return False

        try:
            int(self.current_guess)
        except ValueError:
            print("Your guess contained non numeric values, please only use digits 0-9")
            return False

        self.number_of_guesses += 1
        return True

    def check_guess(self) -> bool:
        """Checks `self.current_guess` against `self.goal` to calculate the number of cows and bulls. Returns the result to the player.

        Returns:
            bool: Status of the check. Only returns True if `self.goal` exactly matches `self.goal`
        """

        if self.current_guess == self.goal:
            return True

        bulls: int = self.bull_counter()
        cows: int = self.cow_counter(bulls)

        print(f"The guess {self.current_guess} contains {cows} cows and {bulls} bulls")

        return False

    def bull_counter(self) -> int:
        """Calculate the number of bulls between `self.goal` and `self.current_guess`

        Returns:
            int: Number of Bulls in `self.current_guess`
        """

        bull_counter = 0
        for counter in range(self.goal_length):
            if self.current_guess[counter] == self.goal[counter]:
                bull_counter += 1

        return bull_counter

    def cow_counter(self, bulls: int) -> int:
        """Calculate the number of cows between `self.goal` and `self.current_guess`

        Args:
            bulls (int): The number of bulls previously calculated

        Returns:
            int: The number of cows in `self.current_guess`
        """

        cow_counter = 0

        current_guess_map: Counter[str] = Counter(self.current_guess)

        for char in self.current_guess:
            current_guess_map[f"{char}"] += 1

        for key in current_guess_map:
            try:
                digit_goal_count = self.goal_map[f"{key}"]
                digit_count_current = current_guess_map[f"{key}"]
                if digit_count_current <= digit_goal_count:
                    cow_counter += digit_count_current
                else:
                    cow_counter += digit_goal_count
            except KeyError:
                pass
        cow_counter -= bulls

        return cow_counter

    def make_guess(self) -> None:
        """User input that overwrites `self.current_guess`"""
        guess = input(
            f"Enter your guess, it must be a number {self.goal_length} digits long: "
        )
        self.current_guess = guess

    def rules(self) -> None:
        """Print the rules to the console"""
        print(f"""
        -- Welcome to cows and bulls, heres how to play! -- \n
            1. Your goal is to guess the randomly generated number \n
            2. You have an infinite number of guesses to do so, but try to get the least possible \n
            3. For this game the number generated is {self.goal_length} digits long, and can have multiple of the same digit \n
            4. After a guess you will be given a number of cows; the correct digits in the wrong place, and bulls; correct guesses in the correct place. 
               A bull cannot also be a cow 
        """)

    def play(self) -> None:
        """Coordinator function for `Cows_And_Bulls`. On function call beings game logic and returns on game completion"""

        self.rules()

        while True:
            self.make_guess()

            if not self.validate_guess():
                continue
            if not self.check_guess():
                continue

            print(
                f"Congrats, you win! \n You guessed the correct answer in {self.number_of_guesses} guesses"
            )
            return


def main() -> None:
    """Initialise and run game `Cows_And_Bulls`"""
    game = Cows_And_Bulls()
    # print(game.goal) # uncomment for dev use
    game.play()
