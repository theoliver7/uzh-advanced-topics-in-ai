import pandas

from conf import MOVIE_NET_INDEX
from WikiDataApiWrapper import WikiDataApiWrapper


class ImageResponseGenerator:
    def __init__(self):
        self.wiki_data_api: WikiDataApiWrapper = WikiDataApiWrapper()
        self.image_df = pandas.read_pickle(MOVIE_NET_INDEX)

    def generate_image_response(self, wiki_data_id):
        # good idea but better to put a link
        """
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
        """
        imdb_id = self.wiki_data_api.get_imdb_id(wiki_data_id)
        return f"https://www.imdb.com/name/{imdb_id}/"
