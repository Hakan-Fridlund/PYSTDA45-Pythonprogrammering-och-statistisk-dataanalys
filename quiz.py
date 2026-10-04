"""
Assignment: Quiz Application with both multiple choice questions and open questions.
- a name variable that is used throughout the quiz
- random order of the questions
- option to restart the quiz after finishing
- case insensitive answers for questions
- add hidden menu when writing admin as name, requiring a password to access the menu

SUGGESTED IMPROVEMENTS:
- use command line arguments when starting file to access the admin menu (argparse) 
- admin menu to add new questions to the quiz
- save the questions to a file and load them when starting from a file (JSON format)
- save the highscore to the same file and load it when starting, showing top 5 after the quiz
- option for user to change how many questions are asked in the quiz, and what cathegory or mixed
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


# TODO: rewrite this to class instead. 2 subclasses for multiple choice questions and open questions.
# text, answer, type, options (for multiple choice questions) and category
# methods: check_answer()

questions = [
    {
        "type": "mcq",                     # mcp = multiple choice question
        "q": "Hur många länder finns det i världen?",
        "options": ["195", "210", "95"],
        "answer": 1,
        "points": 3
    },
    {
        "type": "open",                      # open = open question
        "q": "Vilket land bor vi i?",
        "answer": "Sverige",
        "points": 1
        },
    {
        "type":"open",
        "q": "Vad blir 5*2 ?",
        "answer": "10",
        "points": 2
    },
    {
        "type": "mcq",
        "q": "Hur många ben har normalt en hund?",
            "options": ["3", "2", "4"],
            "answer": 3,
            "points": 1
    },
    {
        "type": "mcq",
        "q": "Vilken planet är närmast solen?",
        "options": ["Venus", "Merkurius", "Mars"],
        "answer": 2,
        "points": 2
    },
    {
        "type": "mcq",
        "q": "Vilket land har flest invånare?",
        "options": ["Indien", "USA", "Kina"],
        "answer": 1,
        "points": 3
    },
]
# TODO: add CLASS for quiz. Attributes: title, questions (lista of Question-objects), cathegory or mixed, number of questions to ask
# Methods: add_question(question), randomize_questions()

# TODO: add CLASS Player, Keeps track of name and result
# Attribut: name, score, answers_given (historik) 
# Methods: answer_question(question, answer), get_score()

# TODO: add function load_questions_from_file(path): before starting

# TODO: add admin menu function to add and remove questions, change password, view highscore, etc.

# TODO: add functions to use in the admin menu and save the question after adding it automatically

# TODO: add function to get_answer(question) to get the answer from the user and check if it is correct with defend against invalid input from the user

# TODO: rewrite to a function to make it more readable and maintainable get_user_name()
name = input("Vad heter du? ")
if name.lower().strip() == "admin":
    password_input = input("Ange lösenord: ")
    if PASSWORD == password_input:
        print("Välkommen till admin-menyn!")
        # Admin menu code function call can be placed here
    else:
        print("Fel lösenord! Du har inte tillgång till admin-menyn.")

print(f"Hej {name}, välkommen till quizzet!")



# TODO: rewrite to a function to make it more readable and maintainable def run_quiz():
while True:
    random.shuffle(questions) # shuffles the questions in random order each time the quiz is run

    for question in questions:
        max_points += int(question["points"])  # adds the count for max points for each question
        print(question["q"])
        if question["type"] == "mcq":
            answer = input(
                f"(1) {question['options'][0]} \n"
                f"(2) {question['options'][1]} \n"
                f"(3) {question['options'][2]})\n"
                "Välj ett alternativ: "
            )

            if int(answer) == question["answer"]:
                score +=int(question["points"])
                print("\nRätt svar!\n")
            else:
                print("\nFel svar!\n")

        elif question["type"] == "open":
            answer = input("Vad är svaret? :")
            if answer.lower().strip() == question["answer"].lower():
                score +=int(question["points"])
                print("\nRätt svar!\n")
            else:
                print("\nFel svar!\n")
        else:
            print("Felaktig fråge-typ!") # error mseeage if question type is not recognized


    if score < 8:
        print(f"{name} du fick {score} poäng av {max_points} möjliga. Försök igen!")
    else:
        print(f"{name} du fick {score} poäng av {max_points} möjliga. Bra jobbat!")

    if score > highscore:
        highscore = score
        print("Grattis till ny highscore!")
    else:
        print(f"Inte bästa resultatet {name}, nuvarande highscore är {highscore}!")

    play_again = input(f"\nVill du spel igen {name}? (Y/N)").lower().strip()
    if play_again == "y":
        score = 0   # reset score to 0 when playing again
        max_points = 0  # reset max_points to 0 when playing again
    else:
        print("Tack för din tid, välkommen åter!")
        break
