"""
Assignment: Quiz Application
"""


score = 0
max_points = 0
highscore = 0
questions = [
    {
        "type": "mcq",
        "q": "Hur många länder finns det i världen?",
        "options": ["195", "210", "95"],
        "answer": 1,
        "points": 3
    },
    {
        "type": "open",
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

name = input("Vad heter du? ")

"""
ToDo: add random question order
"""

while True:
    for question in questions:
        max_points += int(question["points"])
        print(question["q"])
        if question["type"] == "mcq":
            answer = input(f"Välj ett alternativ (1) {question['options'][0]}, (2) {question['options'][1]}, (3) {question['options'][2]}): ")
            if int(answer) == question["answer"]:
                score +=int(question["points"])
                print("Rätt svar!")
            else:
                print("Fel svar!")

        elif question["type"] == "open":
            answer = input("Vad är svaret? :")
            if answer.lower() == question["answer"].lower():
                score +=int(question["points"])
                print("Rätt svar!")
            else:
                print("Fel svar!")



    if score < 8:
        print(f"{name} du fick {score} poäng av {max_points} möjliga. Försök igen!")
    else:
        print(f"{name} du fick {score} poäng av {max_points} möjliga. Bra jobbat!")

    if score > highscore:
        highscore = score
        print(f"Grattis {name} ny highscore!")
    else:
        print(f"Inte bästa resultatet {name}, nuvarande highscore är {highscore}!")

    play_again = input(f"Vill du spel igen {name}? (Y/N)").lower()
    if play_again == "y":
        score = 0
        max_points = 0
        continue
    else:
        print("Tack för din tid!")
        break
