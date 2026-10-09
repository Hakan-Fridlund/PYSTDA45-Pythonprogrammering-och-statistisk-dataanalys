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

SUGGESTED IMPROVEMENTS:
- use command line arguments when starting file to access the admin menu (argparse) 
- save highscore to same file and load when starting, showing top 5 after the quiz.
- use encrypted password for admin menu, saved as hash or salted hash, not plain text
- being able to change password for admin menu from within the admin menu
"""

import random
import json
import pickle
import argparse
import os
import hashlib

CATEGORIES = ("matematik", "natur", "geografi") # tuple for categories constant
score = 0
max_points = 0
highscore = 0
PASSWORD = "admin123"  # TODO: password for admin menu should be salted hash and saved in file

class Question:
    """quiz question with a text(the question) and a correct answer.

    check_answer() compares a given answer to the correct one.
    """

    def __init__(self, text, answer, category):
        self.text = text
        self.answer = answer
        self.category = category

    def __str__(self):
        return (f"Question: {self.text}\nAnswer: {self.answer}\nCategory: {self.category}")

    def check_answer(self, given_answer):
        return given_answer == self.answer

    @classmethod
    def save_to_file(cls, questions_list, path="quiz_questions.pkl"):
        """Class method to save a list with questions to file."""
        try:
            with open(path, "wb") as file:
                pickle.dump(questions_list, file)
            print(f"Frågorna har sparats framgångsrikt i {path}!")
        except Exception as e:
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
        except Exception as e:
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
        return (f"Number of questions: {self.number_of_questions}\nQuestions: {self.questions}\nCategory: {self.category}")


def admin_menu(all_questions):
    """ Runs the hidden admin menu to call admin functions"""
    while True:
        print("\nAdmin menu")
        print("1. Add question")
        print("2. Show questions")
        print("3. Remove question")
        print("4. Change password")
        print("5. View highscore")
        print("6. Exit admin menu")
        choice = get_menu_choice(["1", "2", "3", "4", "5", "6"], "Välj ett alternativ (1-6): ")

        match choice:
            case "1":
                add_question(all_questions)
            case "2":
                show_questions(all_questions)
            case "3":
                remove_question(all_questions)
            case "4":
                change_password()
            case "5":
                view_highscore()
            case "6":
                Question.save_to_file(all_questions)
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
    type = get_menu_choice(["1","2"],"Vill du lägga till en öppen eller flervalsfråga?\n"
                            "(1) för öppen fråga\n(2) för flervalsfråga\n: ")
    text = input("Ange din fråga: ")
    if type == "1":
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


def change_password():
    ...
def view_highscore():
    ...
def check_if_highscore(score):
    ...
# TODO load encrypted password from file
def load_password(path):
    ...


# TODO:  add name from argparse if written
def get_user_name():
    """get and return the user name, strip whitespace and capitalize first letter of each word"""
    return input("Vad heter du? ").strip().lower().title()

def is_valid_category(category):
    """ checks if the category is valid in the Categories list and returns True/False"""
    return category in CATEGORIES or category == "blandat"

# should return True/False
def check_password(password):
    if PASSWORD == password:
        return True
    else:
        return False


def run_quiz(current_quiz):
    """runs the quiz loop, prints questions, receive input, check if answer is correct and handles points"""
    score = 0
    
    for q in current_quiz.questions:
        print(f"\nKategori: {q.category}")
        print(f"Fråga: {q.text}")
        
        # We control if the object is a multiple choice question
        if isinstance(q, MultipleChoiceQuestion):
            letters = "abcd"
            for i, option in enumerate(q.options):
                print(f"  {letters[i]}) {option}")
                
        guess = input("\nDitt svar: ").strip().lower()
        
        if q.check_answer(guess):
            print("Rätt svar! 🎉\n\n")
            score += 1
        else:
            print(f"Tyvärr fel, rätt svar var: {q.answer}")
            
    print(f"\nQuizet är slut! Du fick {score} av {len(current_quiz.questions)} rätt.")
    
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


def run_quiz(current_quiz):
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

    print(f"\nQuizet är slut! Du fick {score} av {len(current_quiz.questions)} rätt.")
    check_if_highscore(score)

    return score

def main():
    """Main function, loads questions at start and then connects all input and menus in order."""
    all_questions = Question.load_from_file()  #Load questions from file at the start of the program
    print("Välkommen!")

    while True:
        name = get_user_name()

        if name == "Admin":
            if check_password(input("Ange lösenord: ")):
                admin_menu(all_questions)
                continue
                # when admin logs out, we move to next iteration of the loop (or break if you want to exit)
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
        run_quiz(my_quiz)
        play_again = get_menu_choice(["y","n"], prompt="Vill du spela igen? (y/n): ")
        if play_again == "n":

            view_highscore()
            print("Tack för din tid, välkommen åter!")
            break

main()
