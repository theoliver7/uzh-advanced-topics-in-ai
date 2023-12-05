import statistics
import sys

import pandas as pd

from conf import CROWD_SOURCING_CSV, BOT_BASE_PATH, BOT_BOT_PATH

sys.path.append(BOT_BOT_PATH)
sys.path.append(BOT_BASE_PATH)

import re
import time
from util.graph import Graph
from util.llm import LLM
from util.question_analyser import QuestionAnalyser
from util.multimedia_classifier import MultimediaClassifier
from util.image_response import ImageResponseGenerator


class Bot:

    def __init__(self):
        self.llm = LLM()
        self.graph = Graph()
        self.analyser = QuestionAnalyser()
        self.multimedia_classifier = MultimediaClassifier()
        self.image_responder = ImageResponseGenerator()
        self.times = []
        self.crowd_source = pd.read_csv(CROWD_SOURCING_CSV,
                                        index_col=0)
        print("---READY FOR OPERATION---")

    def ask(self, message):
        # try:
        print("___________________________________________________________________________________________________")
        print("Question:", message)
        start = time.perf_counter()
        movie_titles, names = self.analyser.get_movie_title(message)

        if self.multimedia_classifier.is_multimedia_request(message):
            print("Handling question as Multimedia")
            image_found = False

            if len(names) > 0:
                names = names[0][0]
                imdb_id = self.graph.get_imdb(names)
                image = self.image_responder.generate_image_response(imdb_id)

                if image != 0:
                    response = f"Here is a Picture of {names} image: {image}"
                    image_found = True

            # Check the flag to set the response if no image was found
            if not image_found:
                response = "Mhh looks like I didn't find a picture"
            return response
        else:
            # CROWD SOURCING
            crowd_disclaimer = None
            if len(movie_titles) > 0:
                entity = self.graph.movie_dict.get(movie_titles[0])
                if isinstance(entity, list):
                    entity = entity[0]
                crowd_match = self.crowd_source[self.crowd_source['Input1ID'].str.contains(entity, na=False)]
                if not crowd_match.empty:
                    crowd_disclaimer = f'[Crowd, inter-rater agreement {crowd_match["FleissKappa"].iloc[0]}, The answer distribution for this specific task was {crowd_match["CORRECT"].iloc[0]} support votes, {crowd_match["INCORRECT"].iloc[0]} reject votes]'

            # GENERATE RESPONSE
            movie_data = self.graph.get_film_info(movie_titles)

            if movie_data:
                response = self.llm.ask_about_movies(question=message, data=movie_data)
            else:
                response = self.llm.ask_no_data(message)

            # Remove everything when the llm thinks it needs to generate more questions and answers
            split_pattern = re.compile(r'<|im_end|>', re.I)
            response = split_pattern.split(response)[0]

            if crowd_disclaimer:
                response = response + "\n" + crowd_disclaimer

        print("POSTING RESPONE:", response)
        end = time.perf_counter()
        self.times.append(end - start)
        print(f"Took: {end - start} seconds,avg: {statistics.mean(self.times)}")
        return response
