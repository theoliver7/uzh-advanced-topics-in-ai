import pickle
from fuzzywuzzy import process

class QuestionAnalyser:
    def __init__(self):
        with open('../dataset/film_dict.pickle', 'rb') as f:
            self.film_dict = pickle.load(f)

    def get_movie_title(self,query):
        # Extract all movie titles from your dictionary
        movie_titles = list(self.film_dict.keys())

        # Use fuzzywuzzy to find the closest match in your dictionary to the user query
        best_match = process.extract(query, movie_titles, limit=2)

        # best_match is a tuple containing the best matching movie title and a score
        # matching_movie_title, score = best_match
        matched_movies = []
        for movie in best_match:
            if int(movie[1]) > 86:
                matched_movies.append(movie[0])
        return sorted(matched_movies, key=len, reverse=True)