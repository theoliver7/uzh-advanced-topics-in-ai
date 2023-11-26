import re


class MultimediaClassifier:
    def __init__(self):
        self.image_keywords = [
            "picture of", "display the", "look like", "looks like", "photo of", "movie poster",
            "cover of", "trailer of", "image of", "cast of", "scene from", 'poster', 'picture', 'image', 'potrait',
            'photo', 'photograph', 'show me'
        ]

    def is_multimedia_request(self, sentence):
        for keyword in self.image_keywords:
            if re.search(keyword, sentence, re.IGNORECASE):
                return True
        return False
