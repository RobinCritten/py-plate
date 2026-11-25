from collections import Counter
from random import randint


class Cows_And_Bulls:
    goal_length: int
    goal: str
    goal_map: dict[str, int]

    number_of_guesses: int = 0
    current_guess: str

    def __init__(self, goal_length: int = 5):
        self.goal_length = goal_length
        self.generate_goal()
        self.goal_map: Counter = Counter(self.goal)

    def generate_goal(self) -> None:

        digit_collection: str = ""

        for _ in range(self.goal_length):
            digit_collection += str(randint(0, 9))

        self.goal = digit_collection

    def validate_guess(self) -> bool:

        # check is correct length
        if len(self.current_guess) != self.goal_length:
            print(
                f"Your guess was {len(self.current_guess)} digits long, please make sure your guess is the correct length ({self.goal_length})"
            )
            return False

        # check is number
        try:
            int(self.current_guess)
        except ValueError:
            print("Your guess contained non numeric values, please only use digits 0-9")
            return False

        # return true if checks pass
        self.number_of_guesses += 1
        return True

    def check_guess(self) -> bool:
        # check guess against goal, return true is matched
        if self.current_guess == self.goal:
            return True

        bulls: int = self.bull_counter()
        cows: int = self.cow_counter(bulls)

        print(f"The guess {self.current_guess} contains {cows} cows and {bulls} bulls")

        return False

    def bull_counter(self) -> int:
        bull_counter = 0
        for counter in range(self.goal_length):
            if self.current_guess[counter] == self.goal[counter]:
                bull_counter += 1

        return bull_counter

    def cow_counter(self, bulls: int) -> int:
        cow_counter = 0

        current_guess_map: Counter = Counter(self.current_guess)

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
        # retrieve user input
        guess = input(
            f"Enter your guess, it must be a number {self.goal_length} digits long: "
        )
        self.current_guess = guess

    def rules(self) -> None:
        # print the game rules
        pass

    def play(self) -> None:

        while True:
            self.make_guess()

            if not self.validate_guess():
                continue
            if not self.check_guess():
                continue

            print("Congrats, you win!")
            print(f"You guessed the correct answer in {self.number_of_guesses} guesses")
            return


def main():
    game = Cows_And_Bulls()
    print(game.goal)
    game.play()


# may be worth making the game a class with attributes digits, n.o. guesses etc?
