import torch
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

from config.conf import MOVIES_CSV_PATH, RATING_CSV_PATH

class Recommender:
    def __init__(self, n_neighbors=3):
        self.n_neighbors = n_neighbors
        movies = pd.read_csv(MOVIES_CSV_PATH)
        ratings = pd.read_csv(RATING_CSV_PATH)
        df = pd.merge(ratings, movies, on='movieId')
        self.user_movie_ratings = df.pivot_table(index='userId', columns='title', values='rating')
        # NaN means user hasn't rated the movie
        self.user_movie_ratings = self.user_movie_ratings.fillna(0)

        # Convert the dataframe to a PyTorch tensor
        self.tensor_ratings = torch.tensor(self.user_movie_ratings.values)

        # Split the data into training and testing sets
        train_data, test_data = train_test_split(self.tensor_ratings.numpy(), test_size=0.2, random_state=42)

        # Create tensors for training and testing sets
        X_train, y_train = torch.from_numpy(train_data[:, 1:]), torch.from_numpy(train_data[:, 0])
        X_test, y_test = torch.from_numpy(test_data[:, 1:]), torch.from_numpy(test_data[:, 0])

        # Initialize the KNN model
        # be carefull TUNE THE NUMBER OF NEIGHBORS
        knn_model = KNeighborsClassifier(n_neighbors=self.n_neighbors)

        knn_model.fit(X_train, y_train)

        predictions = knn_model.predict(X_test)

        accuracy = accuracy_score(y_test, predictions)
        print(f'Accuracy: {accuracy * 100:.2f}%')

    def submit_entry(self, targeted_user, new_user_ratings) -> None:
        """

        Args:
            notation: {'Inception': 5}

        Returns:

        """
        new_user_row = pd.Series(new_user_ratings, name=targeted_user)
        self.user_movie_ratings = self.user_movie_ratings.append(new_user_row)
        self.user_movie_ratings = self.user_movie_ratings.fillna(0)
        self.tensor_ratings = torch.tensor(self.user_movie_ratings.values)

    def get_neighbors(self, targeted_user) -> [str]:
        train_data, test_data = train_test_split(self.tensor_ratings.numpy(), test_size=0.2, random_state=42)

        X_train, y_train = torch.from_numpy(train_data[:, 1:]), torch.from_numpy(train_data[:, 0])

        knn_model = KNeighborsClassifier(n_neighbors=3)
        knn_model.fit(X_train, y_train)

        # Get the indices of the n+1 and n+2 nearest neighbors for the new user
        new_user_index = self.user_movie_ratings.index.get_loc(targeted_user)
        neighbors_indices = knn_model.kneighbors(X_train[new_user_index].reshape(1, -1), n_neighbors=self.n_neighbors, return_distance=False)[0][1:]

        neighbors_usernames = self.user_movie_ratings.iloc[neighbors_indices].index.tolist()

        print(f"Neighbors for 'NewUser': {neighbors_usernames}")

        return neighbors_usernames