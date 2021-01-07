# Quizzler

import data
from question_model import Question
from quiz_brain import QuizBrain
from ui import QuizInterface


question_bank = []
# fill up the question bank list with Question objects
for dic in data.load_data():
    question_bank.append(Question(dic["question"], dic["correct_answer"]))

# initialize the quiz brain
qb = QuizBrain(question_bank)
# initialize the GUI
qi = QuizInterface(qb)
