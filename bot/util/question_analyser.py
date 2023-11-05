import pickle
from fuzzywuzzy import process

from config.conf import FILM_PICKLE_PATH


class QuestionAnalyser:
    def __init__(self):
        with open(FILM_PICKLE_PATH, 'rb') as f:
            self.film_dict = pickle.load(f)
        self.movie_titles = list(self.film_dict.keys())

    def get_movie_title(self,query):
        # Extract all movie titles from your dictionary


        # Use fuzzywuzzy to find the closest match in your dictionary to the user query
        best_match = process.extract(query, self.movie_titles, limit=2)

        # best_match is a tuple containing the best matching movie title and a score
        # matching_movie_title, score = best_match
        matched_movies = []
        for movie in best_match:
            print("FUZZYWUZZY results:",movie)
            if int(movie[1]) > 86:
                matched_movies.append(movie[0])
        return sorted(matched_movies, key=len, reverse=True)