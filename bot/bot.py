import sys
sys.path.append('/home/oliver/dev/uzh/atai_bot/bot')
sys.path.append('/home/oliver/dev/uzh/atai_bot')
import re
from util.graph import Graph
from util.llm import LLM
from util.question_analyser import QuestionAnalyser


class Bot:

    def __init__(self):
        self.llm = LLM()
        self.graph = Graph()
        self.analyser = QuestionAnalyser()
        print("---READY FOR OPERATION---")

    def ask(self, message):
        movie_titles = self.analyser.get_movie_title(message)

        movie_data = self.graph.get_film_info(movie_titles)

        if movie_data:
            response = self.llm.ask_about_movies(question=message, data=movie_data)
        else:
            response = self.llm.ask_no_data(message)

        # Remove everything when the llm thinks it needs to generate more questions and answers
        split_pattern = re.compile(r'Question:|Answer:|QUESTION:|ANSWER:', re.I)
        response = split_pattern.split(response)[0]


        print("POSTING RESPONE:",response)

        return response
