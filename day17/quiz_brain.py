class QuizBrain:
    def __init__(self, questions_list):
        self.question_number = 0
        self.questions_list = questions_list
        self.score = 0

    def next_question(self):
        """Displays and processes the next question."""
        # the Q number in the text needs to start from 1
        print(f"Q.{self.question_number + 1}: {self.questions_list[self.question_number].text} (True/False)?")
        while True:
            choice = input("> ").lower()
            if choice in ["true", "false"]:
                break
            print(f"Invalid choice. Please type \"True\", \"False\".")
        self.check_answer(choice, self.questions_list[self.question_number].answer)
        # only increase this once the current question is completed
        self.question_number += 1

    def still_has_questions(self):
        """Checks if there are questions remaining and returns a BOOL."""
        if self.question_number < len(self.questions_list):
            return True
        return False

    def check_answer(self, choice, answer):
        """Takes two STR and compares them, then prints the result and score."""
        if choice == answer.lower():
            print("You got it right!")
            self.score += 1
        else:
            print("That's wrong.")
        # show the correct answer either way
        print(f"The correct answer was: {answer}.")
        # show the number of correct / total answers
        # again it needs + 1 since the printed value starts with 1
        print(f"Your current score is: {self.score}/{self.question_number + 1}.")
        # print an empty line between the questions
        print()
