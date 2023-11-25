import statistics
import sys

import pandas as pd

sys.path.append('/home/oliver/dev/uzh/atai_bot/bot')
sys.path.append('/home/oliver/dev/uzh/atai_bot')
import re
import time
from util.graph import Graph
from util.llm import LLM
from util.question_analyser import QuestionAnalyser


class Bot:

    def __init__(self):
        self.llm = LLM()
        self.graph = Graph()
        self.analyser = QuestionAnalyser()
        self.times = []
        self.crowd_source = pd.read_csv("/home/oliver/dev/uzh/atai_bot/dataset/crowd_data/crowd-sourcing-output.csv",
                                        index_col=0)
        print("---READY FOR OPERATION---")

    def ask(self, message):
        print("Question:", message)
        start = time.perf_counter()
        movie_titles = self.analyser.get_movie_title(message)
        entity = self.graph.movie_dict[movie_titles[0]]
        crowd_match = self.crowd_source[self.crowd_source['Input1ID'].str.contains(entity, na=False)]
        crowd_disclaimer = None
        if not crowd_match.empty:
            crowd_disclaimer = f'[Crowd, inter-rater agreement {crowd_match["FleissKappa"].iloc[0]}, The answer distribution for this specific task was {crowd_match["CORRECT"].iloc[0]} support votes, {crowd_match["INCORRECT"].iloc[0]} reject votes]'

        movie_data = self.graph.get_film_info(movie_titles)

        if movie_data:
            response = self.llm.ask_about_movies(question=message, data=movie_data)
        else:
            response = self.llm.ask_no_data(message)

        # Remove everything when the llm thinks it needs to generate more questions and answers
        # ONLY
        # ANSWER
        # THIS
        # If this question is not related to movies, kindly let the user know to focus on movie-related topics.
        split_pattern = re.compile(r'<|im_end|>', re.I)
        response = split_pattern.split(response)[0]
        if crowd_disclaimer:
            response = response +"\n"+ crowd_disclaimer
        print("POSTING RESPONE:", response)
        end = time.perf_counter()
        self.times.append(end - start)
        print(f"Took: {end - start} seconds,avg: {statistics.mean(self.times)}")
        return response
