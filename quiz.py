"""
Assignment: Quiz Application with both multiple choice questions and open questions.
- a name variable that is used throughout the quiz
- random order of the questions
- option to restart the quiz after finishing
- case insensitive answers for questions
Added features:
- hidden menu when writing admin as name, requiring a password to access the menu
- admin menu to add new questions to the quiz
- save the questions to a file and load them when starting from a file (pkl) format)
- option for user to change how many questions are asked in the quiz, and what category or mixed
- defended against invalid input from the user
- rewritten the code to classes and functions to make it more readable and maintainable
- separated code and data, read questions, highscore and secure password from file
- save highscore to file and load when starting, showing top 10 after the quiz is done.

SUGGESTED IMPROVEMENTS:
- use command line arguments when starting file to access the admin menu (argparse) 
"""

import random
import json
import pickle
from pickle import UnpicklingError
import argparse
import os
import sys

CATEGORIES = ("matematik", "natur", "geografi") # tuple for categories constant
highscore = {}
PASSWORD = "admin123"
class Question:
    """quiz question with a text(the question) and a correct answer.

    check_answer() compares a given answer to the correct one.
    """

    def __init__(self, text, answer, category):
        self.text = text
        self.answer = answer
        self.category = category

    def __str__(self):
        return f"Question: {self.text}\nAnswer: {self.answer}\nCategory: {self.category}"

    def check_answer(self, given_answer):
        return given_answer == self.answer

    @classmethod
    def save_to_file(cls, questions_list, path="quiz_questions.pkl"):
        """Class method to save a list with questions to file."""
        try:
            with open(path, "wb") as file:
                pickle.dump(questions_list, file)
            print(f"Frågorna har sparats framgångsrikt i {path}!")
        except OSError as e:
            print(f"Ett fel uppstod när filen skulle sparas: {e}")

    @classmethod
    def load_from_file(cls, path="quiz_questions.pkl"):
        """Class method to load and return a list with question from file."""
        if not os.path.exists(path):
            print(f"Hittade inte '{path}'. Returnerar en tom lista.")
            return []
        try:
            with open(path, "rb") as file:
                print(f"{path} loaded.")
                return pickle.load(file)
        except UnpicklingError:
            print(f"Fel: Filen '{path}' är korrupt (kan ha öppnats i en texteditor).")
            return []
        except OSError as e:
            print(f"Ett fel uppstod när filen skulle laddas: {e}")
            return []


class OpenQuestion(Question): # pylint: disable=too-few-public-methods
    """Free-text question sub-class. Used only for type checks."""


class MultipleChoiceQuestion(Question):
    """Question subclass with a list of options to choose from."""

    def __init__(self, text, answer, options, category):
        super().__init__(text, answer, category)
        self.options = options
        self.category = category

    def __str__(self):
        options_text = "\n".join(
            f"{i}. {opt}" for i, opt in enumerate(self.options, start=1)
        )
        return (f"Question: {self.text}\n"
                f"Options: {options_text}\n"
                f"Answer: {self.answer}\n"
                f"Category: {self.category}")


class Quiz: # pylint: disable=too-few-public-methods
    """A quiz with a random selection of questions.

    On init: Filters all_questions by category ("mixed" keeps every category),
    shuffles them and keeps the first number_of_questions.
    """
    def __init__(self, all_questions, number_of_questions=3, category="blandat"):
        self.category = category
        self.number_of_questions = number_of_questions

        if category == "blandat":
            pool = all_questions[:]
        else:
            pool = [q for q in all_questions if q.category == category]
        random.shuffle(pool)
        self.questions = pool[:number_of_questions]

    def __str__(self):
        return (f"Number of questions: "
            f"{self.number_of_questions}\nQuestions: {self.questions}\nCategory: {self.category}")


def admin_menu(all_questions, highscore_dict):
    """ Runs the hidden admin menu to call admin functions"""
    while True:
        print("\nAdmin menu")
        print("1. Add question")
        print("2. Show questions")
        print("3. Remove question")
        print("4. View highscore")
        print("5. Exit admin menu")
        choice = get_menu_choice(["1", "2", "3", "4", "5"], "Välj ett alternativ (1-5): ")

        match choice:
            case "1":
                add_question(all_questions)
            case "2":
                show_questions(all_questions)
            case "3":
                remove_question(all_questions)
            case "4":
                view_highscore(highscore_dict)
            case "5":
                Question.save_to_file(all_questions)
                #removes the argparse arguments so the name is not locked to admin or the argument
                sys.argv = [sys.argv[0]]
                break


def get_menu_choice(valid_choices, prompt="Välj ett alternativ: "):
    """used by admin_menu to check against faulty input
    takes list argument with strings of valid choices and prompt"""
    string_choices = [str(choice).strip().lower() for choice in valid_choices]
    while True:
        choice = input(prompt).strip().lower()
        if choice in string_choices:
            return choice
        print("Ogiltigt val, försök igen.\n")


def add_question(all_questions):
    """Adds question by input. appends open och mpc-question to list"""
    category = get_menu_choice(CATEGORIES, f"Välj en kategori {CATEGORIES} ")
    current_type = get_menu_choice(["1","2"],"Vill du lägga till en öppen eller flervalsfråga?\n"
                            "(1) för öppen fråga\n(2) för flervalsfråga\n: ")
    text = input("Ange din fråga: ")
    if current_type == "1":
        answer = input("Ange svaret: ").strip().lower()
        my_question = OpenQuestion(text, answer, category)
    else:
        options = []
        letters = "abcd"
        for i in range(4):
            letter = letters[i]
            user_input = input(f"Ange svarsalternativ {letter}: ").strip().lower()
            options.append(user_input)
        answer = get_menu_choice(["a","b","c","d"],"Vilket är det rätta alternativet (a,b,c,d): ")
        my_question = MultipleChoiceQuestion(text, answer, options, category)

    all_questions.append(my_question)


def show_questions(all_questions):
    """ prints all questions with index and category"""
    if not all_questions:
        print("Listan är tom.")
        return
    for i, q in enumerate(all_questions, start=1):
        print(f"{i}. [{q.category}]) {q.text}")

def remove_question(all_questions):
    """ shows all questions, takes index input to remove from list, 0 to cancel"""
    show_questions(all_questions)
    # creates a list strings of valid inputs from 0 to the length of questions in all_questions
    valid = ["0"] + [str(i) for i in range(1, len(all_questions) + 1)]

    choice = get_menu_choice(valid, "Nummer att ta bort (0 = avbryt): ")
    if choice == "0":
        return
    removed = all_questions.pop(int(choice) - 1)
    print(f"Tog bort: {removed.text}")


def view_highscore(highscore_dict):
    """prints the highscore if available."""
    if not highscore_dict:
        print("Topplistan är tom just nu!")
        return
    print("\n HIGHSCORELISTAN:")
    for name, current_score in highscore_dict.items():
        print(f"{name}: {current_score} poäng")



def check_if_highscore(name, current_score, highscore_dict, max_slots=5):
    """checks if highscore and adds it to the highscore_dict"""
    if len(highscore_dict) < max_slots or current_score > min(highscore_dict.values()):
        highscore_dict[name] = current_score
        print("Snyggt! Du tog en plats på topplistan!")

        # if too many on list, remove the one with least score
        if len(highscore_dict) > max_slots:
            # find the name of the lowest score
            lowest_player = min(highscore_dict, key=highscore_dict.get)
            # removes the player from dict
            highscore_dict.pop(lowest_player)
        view_highscore(highscore_dict)

    else:
        print(f"Tyvärr räckte dina poäng inte hela vägen till topp {max_slots}.")

    return highscore_dict


def load_highscore(path="quiz_highscore.json"):
    """Loads and returns highscorelist from json file.
    if the file is missing or corrupt it will return an empty dict.
    """
    if not os.path.exists(path):
        print(f"Hittade inte '{path}'. Returnerar en tom highscore-lista.")
        return {}

    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        print(f"Fel: Filen '{path}' är korrupt eller felaktigt formaterad.")
        return {}
    except OSError as e:
        print(f"Ett fel uppstod när highscore skulle laddas: {e}")
        return {}


def save_highscore(highscore_dict, path = "quiz_highscore.json"):
    """save a dictionary med highscores to a json file"""
    try:
        with open(path, "w", encoding="utf-8") as file:
            # indent=4 makes this easy to read in external texteditor
            json.dump(highscore_dict, file, indent=4, ensure_ascii=False)
        print(f"Highscore har sparats i {path}!")
    except OSError as e:
        print(f"Ett fel uppstod när highscore skulle sparas: {e}")

def get_user_name():
    """ Uses argparse if provided, otherwise prompts via user input
    get and return the user name, strip whitespace and capitalize first letter of each word"""
    parser = argparse.ArgumentParser(description="Quiz-spel")
    parser.add_argument(
        "-n",
        "--name",
        type=str,
        help="Ange ditt namn direkt vid start av spelet, admin för tillgång till admin menyn"
    )
    #prevents crash if other arguments is added
    args, _ = parser.parse_known_args()

    if args.name:
        name = args.name
    else:
        name = input("Vad heter du? ")

    return name.strip().lower().title()

def is_valid_category(category):
    """ checks if the category is valid in the Categories list and returns True/False"""
    return category in CATEGORIES or category == "blandat"

def check_password(password):
    """checks if password is correct and returns True/False"""
    if PASSWORD == password:
        return True
    else:
        return False


def get_number_of_questions(prompt, max_questions):
    """takes input and checks if it is a integer in the valid interval and returns the number""" 
    while True:
        try:
            number = int(input(prompt))
        except ValueError:
            print(f"Fel, ange ett heltal mellan 1 och {max_questions}")
            continue

        if 1 <= number <= max_questions:
            return number
        print(f"Ange ett heltal mellan 1 och {max_questions}.")


def filter_by_category(all_questions, category):
    """Return list of questions in the category ("blandat" returns all)."""
    if category == "blandat":
        return all_questions[:]
    return [q for q in all_questions if q.category == category]


def run_quiz(name, highscore_dict, current_quiz):
    score = 0

    for q in current_quiz.questions:
        print(f"Fråga: {q.text}")

        # controls if it is multiple choice class
        if isinstance(q, MultipleChoiceQuestion):
            letters = "abcd"
            for i, option in enumerate(q.options):
                print(f"  {letters[i]}) {option}")

        guess = input("\nDitt svar: ").strip().lower()

        if q.check_answer(guess):
            print("Rätt svar! 🎉")
            score += 1
        else:
            print(f"Tyvärr fel, rätt svar var: {q.answer}\n")

    print(f"nQuizet är slut! Du fick {score} av {len(current_quiz.questions)} rätt.")
    check_if_highscore(name, score, highscore_dict, max_slots=5)
    save_highscore(highscore_dict)

    return score

def main():
    """Main function, loads questions at start and then connects all input and menus in order."""
    all_questions = Question.load_from_file()  #Load questions from file at the start of the program
    highscore_dict = load_highscore()

    print("Välkommen!")

    while True:
        name = get_user_name()

        if name == "Admin":
            if check_password(input("Ange lösenord: ")):
                admin_menu(all_questions, highscore_dict)

                # when admin logs out, we move to next iteration of the loop
            else:
                print("Fel lösenord!")
                continue

        # if not admin, we proceed to the next step
        print(f"\nHej {name}, nu kör vi igång quizzet!")
        # checks if category is valid in loop
        while True:
            category = input(f"Välj kategori: {CATEGORIES} eller blandat: ").strip().lower()
            if is_valid_category(category):
                break
            else:
                print("Ogiltig kategori, försök igen.")

        max_questions = len(filter_by_category(all_questions, category))
        number = get_number_of_questions(f"Hur många frågor vill du ha?\n"
            f"Max antal för {category} är {max_questions}: ", max_questions)

        my_quiz = Quiz(all_questions, number, category)
        run_quiz(name, highscore_dict, my_quiz)
        play_again = get_menu_choice(["y","n"], prompt="Vill du spela igen? (y/n): ")
        if play_again == "n":

            view_highscore(highscore_dict)
            print("Tack för din tid, välkommen åter!")
            break

main()
