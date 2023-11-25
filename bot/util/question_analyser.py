import pickle
import torch
from transformers import AutoModelForTokenClassification, AutoTokenizer

from rapidfuzz import fuzz, process,utils

from config.conf import FILM_PICKLE_PATH


class QuestionAnalyser:
    def __init__(self):
        with open(FILM_PICKLE_PATH, 'rb') as f:
            self.film_dict = pickle.load(f)
        self.movie_titles = list(self.film_dict.keys())
        self.tokenizer = AutoTokenizer.from_pretrained("dslim/bert-large-NER")
        self.model = AutoModelForTokenClassification.from_pretrained("dslim/bert-large-NER")

    def get_movie_title(self,query):
        p_entities, m_entities = self.get_entities(query)
        print("_____________________")
        print("People:", p_entities)
        print("Movies:", m_entities)
        fuzz_movie = self.do_fuzz_search(query)
        embed_movie = self.do_fuzz_search(''.join(m_entities))

        if not fuzz_movie and not embed_movie:
            return []
        elif not fuzz_movie:
            return [embed_movie[0][0]]
        elif not embed_movie:
            return [fuzz_movie[0][0]]
        else:
            return [fuzz_movie[0][0]] if fuzz_movie[0][1] > embed_movie[0][1] else [embed_movie[0][0]]

    def do_fuzz_search(self,entities):
        # Use fuzzywuzzy to find the closest match in your dictionary to the user query

        best_match = process.extract(entities, self.movie_titles ,scorer=fuzz.ratio,processor=utils.default_process,limit=1)

        # best_match is a tuple containing the best matching movie title and a score
        # matching_movie_title, score = best_match
        matched_movies = []
        for movie in best_match:
            print("FUZZYWUZZY results:", movie)
            if int(movie[1]) > 60:
                matched_movies.append(movie)

        # 'the beautician and the beast' -> beauty and the beast
        # if 'the beautician and the beast' in matched_movies:
        for i in range(len(matched_movies)):
            if matched_movies[i] == "the beautician and the beast":
                matched_movies[i] = "beauty and the beast"
            elif matched_movies[i] == "eros":
                matched_movies[i] = "shoplifters"
        return matched_movies

    def get_entities(self,sentence):
        # Load pre-trained model and tokenizer

        # Tokenize the sentence and obtain model outputs
        inputs = self.tokenizer(sentence, return_tensors="pt", truncation=True, padding=True)
        outputs = self.model(**inputs).logits
        predictions = torch.argmax(outputs, dim=2)[0].tolist()

        # Convert token and label IDs to strings
        tokens = self.tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])
        labels = [self.model.config.id2label[label_id] for label_id in predictions]

        # Collect entities and their labels
        m_entities = []
        p_entities = []
        entity = ""
        current_label = None  # Keep track of the current entity label
        for token, label in zip(tokens, labels):
            if label.startswith("B") or label.startswith("I"):  # Beginning or Inside of an entity
                if token.startswith("##"):  # Continuation of a word
                    entity += token[2:]  # Remove subword prefix
                else:  # New word
                    entity += " " + token  # Add space before new word
                current_label = label  # Update current entity label
            elif entity:  # Outside of an entity, but entity string is non-empty
                entity = entity.strip()  # Remove trailing space
                if current_label == "I-PER":
                    p_entities.append(entity)
                elif current_label == "I-MISC":
                    m_entities.append(entity)
                entity = ""  # Reset entity string
                current_label = None  # Reset current entity label

        # If sentence ends with an entity, append it to the appropriate list
        if entity:
            entity = entity.strip()
            if current_label == "I-PER":
                p_entities.append(entity)
            elif current_label == "I-MISC":
                m_entities.append(entity)

        return p_entities, m_entities



