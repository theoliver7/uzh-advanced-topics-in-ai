import pandas

from config.conf import MOVIE_NET_INDEX


class ImageResponseGenerator:
    def __init__(self):
        self.image_df = pandas.read_pickle(MOVIE_NET_INDEX)

    def generate_image_response(self, imdb_id):
        filtered_df = self.image_df[
            self.image_df['cast'].str.contains(imdb_id) & self.image_df["type"].str.contains("event")]
        if len(filtered_df) == 0:
            filtered_df = self.image_df[
                self.image_df['cast'].str.contains(imdb_id) & self.image_df["type"].str.contains("publicity")]
        sorted_df = filtered_df.sort_values(by='cast', key=lambda col: col.str.len(), ascending=True)
        if len(sorted_df) > 0:
            return sorted_df['img'].iloc[0].split(".jpg")[0]
        else:
            return 0
