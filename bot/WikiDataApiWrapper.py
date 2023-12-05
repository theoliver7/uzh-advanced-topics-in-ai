import requests
from conf import OMDB_API_KEY


class WikiDataApiWrapper:
    def __init__(self):
        self.pi_key = OMDB_API_KEY

    def get_imdb_id(self, wikidata_id):

        print(f"wikidata_id {wikidata_id}")

        # Wikidata API URL
        url = f"https://www.wikidata.org/w/api.php?action=wbgetclaims&format=json&entity={wikidata_id}"

        # Make a GET request to the Wikidata API
        response = requests.get(url)

        # Check if the request was successful and retrieve the IMDb ID if available
        if response.status_code == 200:
            data = response.json()
            if "P345" in data["claims"]:
                imdb_id = data["claims"]["P345"][0]["mainsnak"]["datavalue"]["value"]
                print(f"The IMDb ID for {wikidata_id} is {imdb_id}")
                return imdb_id
            else:
                print(f"No IMDb ID found for {wikidata_id}")
        else:
            print("Failed to fetch data from Wikidata")
        return ""
