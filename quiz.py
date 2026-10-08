"""
Assignment: Quiz Application with both multiple choice questions and open questions.
- a name variable that is used throughout the quiz
- random order of the questions
- option to restart the quiz after finishing
- case insensitive answers for questions
Added features:
- add hidden menu when writing admin as name, requiring a password to access the menu

SUGGESTED IMPROVEMENTS:
- use command line arguments when starting file to access the admin menu (argparse) 
- admin menu to add new questions to the quiz
- save the questions to a file and load them when starting from a file (JSON format)
- save the highscore to the same file and load it when starting, showing top 5 after the quiz
- option for user to change how many questions are asked in the quiz, and what category or mixed
- defend against invalid input from the user
- show answer key at the end of the quiz
- rewrite the code to classes and functions to make it more readable and maintainable
- add categories to the questions and let the user choose which category to play if wanted
- separate code and data, read questions and highscore from file, no hardcoded questions inside code
- use encrypted password for admin menu, saved as hash or salted hash, not plain text
- being able to change password for admin menu from within the admin menu
"""

import random
import json
import argparse
import os
import hashlib

CATEGORIES = ("matematik", "natur", "geografi") # tuple for categories constant
score = 0
max_points = 0
highscore = 0
PASSWORD = "admin123"  # TODO: password for admin menu should be salted hash and saved in file

class Question:
    """A quiz question with a text(the question) and a correct answer.

    check_answer() compares a given answer to the correct one.
    """

    def __init__(self, text, answer):
        self.text = text
        self.answer = answer

    def __str__(self):
        return f"Question: {self.text}\nAnswer: {self.answer}"

    def check_answer(self, given_answer):
        return given_answer == self.answer


class OpenQuestion(Question):
    """Free-text question sub-class. Used only for type checks."""


class MultipleChoiceQuestion(Question):
    """Question with a list of options to choose from."""

    def __init__(self, text, answer, options):
        super().__init__(text, answer)
        self.options = options

    def __str__(self):
        options_text = "\n".join(
            f"{i}. {opt}" for i, opt in enumerate(self.options, start=1)
        )
        return (f"Question: {self.text}\n"
                f"Options: {options_text}\n"
                f"Answer: {self.answer}")


class Quiz:
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


# TODO: add CLASS Player, Keeps track of name and result
# Attribut: name, score, answers_given (historik) 
# Methods: answer_question(question, answer), get_score()

# TODO: add function load_questions_from_file(path): before starting
def load_questions_from_file(path):
    ...
def save_questions_to_file(path):
    ...

# TODO: add functions to use in the admin menu and save the question after adding it automatically
def admin_menu():
    while True:
        print("Admin menu")
        print("1. Add question")
        print("2. Remove question")
        print("3. Change password")
        print("4. View highscore")
        print("5. Exit admin menu")
        choice = get_menu_choice(["1", "2", "3", "4", "5"], "Välj ett alternativ (1-5): ")

        match choice:
            case "1":
                add_question()
            case "2":
                remove_question()
            case "3":
                change_password()
            case "4":
                view_highscore()
            case "5":
                save_questions_to_file("questions.json")
                break


def get_menu_choice(valid_choices, prompt="Välj ett alternativ: "):
    """used by admin_menu to check against faulty input"""
    string_choices = [str(choice).strip() for choice in valid_choices]
    while True:
        choice = input(prompt).strip()
        if choice in string_choices:
            return choice
        print(f"Ogiltigt val, försök igen.\n {prompt}")


def add_question():
    ...
def remove_question():
    ...
def change_password():
    ...
def view_highscore():
    ...

# TODO: add function to get_answer(question) to get the answer from the user and check if it is correct with defend against invalid input from the user
# check_answer is already available in class question


def get_user_name():
    """get and return the user name, strip whitespace and capitalize first letter of each word"""
    return input("Vad heter du? ").strip().lower().title()

def is_valid_category(category):
    """ checks if the category is valid in the Categories list and returns True/False"""
    return category in CATEGORIES or category == "blandat"

# should return True/False
def check_password(prompt): 
    ...

# this function should print the questions, receive input and check if correct. and handle points     
def run_quiz(quiz):
    ...

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


def main():
    """Main function, loads questions at start and connects all input and menus in order."""
    all_questions = load_questions_from_file("questions.json")  # Load questions from file at the start of the program
    print("Välkommen!")
    
    while True:
        name = get_user_name()
        
        if name == "Admin":
            if check_password(input("Ange lösenord: ")):
                admin_menu()
                # when admin logs out, we move to next iteration of the loop (or break if you want to exit)
            else: 
                print("Fel lösenord!")
                break

        # if not admin, we proceed to the next step
        print(f"Hej {name}, välkommen till quizzet!")
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


main()
