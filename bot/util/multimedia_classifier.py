import re


class MultimediaClassifier:
    def __init__(self):
        self.image_keywords = [
            'picture of', 'display the', 'look like', 'looks like', 'photo of', 'movie poster',
            'cover of', 'trailer of', 'image of', 'cast of', 'scene from', 'poster', 'advertisement', 'flyer', 'picture', 'image', 'potrait',
            'photo', 'photograph', 'photograph of', 'show me', 'illustrate', 'portrait of', 'portraiture', 'Headshot'
            'film poster', 'movie advertisement', 'cinematic poster', 'visual', 'representation',
            'visual representation of', 'present', 'front of', 'jacket', 'jacket of'
        ]

    def is_multimedia_request(self, sentence):

        print(f"is_multimedia_request - sentence {sentence}")

        for keyword in self.image_keywords:
            if re.search(keyword, sentence, re.IGNORECASE) or keyword in sentence:
                print("is_multimedia_request - word finded")
                return True
        print("is_multimedia_request - no word finded")
        return False
