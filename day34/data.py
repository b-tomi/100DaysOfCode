import requests

API_URL = "https://opentdb.com/api.php"
PARAMS = {
    "amount": 12,
    "type": "boolean",
    "category": 18
}


def load_data():
    """Loads the data from the API, returns a LIST."""
    response = requests.get(API_URL, params=PARAMS)
    response.raise_for_status()
    response_json = response.json()
    if response_json["response_code"] == 0:
        return response.json()["results"]
    # if there's an issue, use the offline data instead
    return offline_data


# quiz data from Day 17, to have an offline back-up
offline_data = [
    {"category": "Science: Computers",
     "type": "boolean",
     "difficulty": "easy",
     "question": "Linus Torvalds created Linux and Git.",
     "correct_answer": "True",
     "incorrect_answers": ["False"]},
    {"category": "Science: Computers",
     "type": "boolean",
     "difficulty": "easy",
     "question": "The programming language \"Python\" is based off a modified version of \"JavaScript\".",
     "correct_answer": "False",
     "incorrect_answers": ["True"]},
    {"category": "Science: Computers",
     "type": "boolean",
     "difficulty": "easy",
     "question": "The logo for Snapchat is a Bell.",
     "correct_answer": "False",
     "incorrect_answers": ["True"]},
    {"category": "Science: Computers",
     "type": "boolean",
     "difficulty": "easy",
     "question": "Pointers were not used in the original C programming language; they were added later on in C++.",
     "correct_answer": "False",
     "incorrect_answers": ["True"]},
    {"category": "Science: Computers",
     "type": "boolean",
     "difficulty": "easy",
     "question": "RAM stands for Random Access Memory.",
     "correct_answer": "True",
     "incorrect_answers": ["False"]},
    {"category": "Science: Computers",
     "type": "boolean",
     "difficulty": "easy",
     "question": "Ada Lovelace is often considered the first computer programmer.",
     "correct_answer": "True",
     "incorrect_answers": ["False"]},
    {"category": "Science: Computers",
     "type": "boolean",
     "difficulty": "easy",
     "question": "In most programming languages, the operator ++ is equivalent to the statement \"+= 1\".",
     "correct_answer": "True",
     "incorrect_answers": ["False"]},
    {"category": "Science: Computers",
     "type": "boolean",
     "difficulty": "easy",
     "question": "Time on Computers is measured via the EPOX System.",
     "correct_answer": "False",
     "incorrect_answers": ["True"]},
    {"category": "Science: Computers",
     "type": "boolean",
     "difficulty": "easy",
     "question": "The Windows 7 operating system has six main editions.",
     "correct_answer": "True",
     "incorrect_answers": ["False"]},
    {"category": "Science: Computers",
     "type": "boolean",
     "difficulty": "easy",
     "question": "The NVidia GTX 1080 gets its name because it can only render at a 1920x1080 screen resolution.",
     "correct_answer": "False", "incorrect_answers": ["True"]},
    {"category": "Science: Computers",
     "type": "boolean",
     "difficulty": "easy",
     "question": "Linux was first created as an alternative to Windows XP.",
     "correct_answer": "False",
     "incorrect_answers": ["True"]},
    {"category": "Science: Computers",
     "type": "boolean",
     "difficulty": "easy",
     "question": "The Python programming language gets its name from the British comedy group \"Monty Python.\"",
     "correct_answer": "True",
     "incorrect_answers": ["False"]}
]
