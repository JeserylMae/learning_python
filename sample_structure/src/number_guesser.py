import os
import random
from src.mixins import ScoreMixin
from datetime import datetime


class NumberGuesser(ScoreMixin):
    def __init__(self):
        self.data_folder = "data"
        self.score_file = os.path.join(self.data_folder, "highest_score.txt")
        self.highest_score_date_file = os.path.join(self.data_folder, "highest_score_date.txt")
        
        super().__init__(self.score_file)
        self.create_data_folder()

    def create_data_folder(self):
        if not os.path.exists(self.data_folder):
            os.makedirs(self.data_folder)

    def load_highest_score_date(self):
        if os.path.exists(self.highest_score_date_file):
            with open(self.highest_score_date_file, "r") as file:
                return file.read()
        return None

    def save_highest_score_and_date(self, score, date):
        try:
            with open(self.score_file, "w") as file:
                file.write(str(score))
            with open(self.highest_score_date_file, "w") as file:
                file.write(date)
        except IOError:
            print("Error: Unable to save score and date.")

    def play_name_guesser(self):
        secret_number = random.randint(1, 100)
        attempts = 0

        print("Try to guess the secret number between 1 and 100!")
        print("Enter 'q' to quit.")

        while True:
            guess = input("Enter your guess: ")
            if guess.lower() == 'q':
                print("Quitting the game.")
                break

            if not guess.isdigit():
                print("Please enter a valid number.")
                continue

            guess = int(guess)
            attempts += 1

            if guess < secret_number:
                print("Too low! Try again.")
            elif guess > secret_number:
                print("Too high! Try again.")
            else:
                print(f"Congratulations! You guessed the number in {attempts} attempts.")
                highest_score = self.load_highest_score()
                highest_score_date = self.load_highest_score_date()
                if highest_score is None or attempts < highest_score:
                    if highest_score is not None:
                        print(f"NEW RECORD! Previous Record: {highest_score} (Achieved on: {highest_score_date})")
                    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self.save_highest_score_and_date(attempts, current_datetime)
                else:
                    print(f"FAIL TO ACHIEVE NEW RECORD. CURRENT RECORD: {highest_score} (Achieved on: {highest_score_date})")
                break

    def display_menu(self):
        print("\nMenu:")
        print("1. Start Game")
        print("2. View Highest Score")
        print("3. Quit")

    def start(self):
        while True:
            self.display_menu()
            choice = input("Enter your choice: ")
            if choice == '1':
                self.play_name_guesser()
            elif choice == '2':
                highest_score = self.load_highest_score()
                highest_score_date = self.load_highest_score_date()
                if highest_score is not None:
                    print(f"Highest Score: {highest_score} (Achieved on: {highest_score_date})")
                else:
                    print("No highest score recorded yet.")
            elif choice == '3':
                print("Exiting the game.")
                break
            else:
                print("Invalid choice. Please try again.")