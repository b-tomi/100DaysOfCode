import html


class QuizBrain:

    def __init__(self, questions_list):
        self.question_number = 0
        self.questions_list = questions_list
        self.score = 0

    def next_question(self):
        """Returns the next question as STR."""
        # in order to keep changes to the original code from Day 17 to a minimum, have to increase this now
        self.question_number += 1
        # unescape characters in the question text if necessary
        fixed_text = html.unescape(self.questions_list[self.question_number - 1].text)
        # the displayed question number doesn't need the + 1 anymore
        return f"Q.{self.question_number}: {fixed_text}"

    def still_has_questions(self):
        """Checks if there are questions remaining and returns a BOOL."""
        if self.question_number < len(self.questions_list):
            return True
        return False

    def check_answer(self, choice):
        """Takes a STR, compares it to the current answer and returns a BOOL."""
        if choice == self.questions_list[self.question_number - 1].answer:
            self.score += 1
            return True
        return False
