import pickle

import torch
from rapidfuzz import fuzz, process, utils
from transformers import AutoModelForTokenClassification, AutoTokenizer

from conf import FILM_PICKLE_PATH, HUMAN_PICKLE_PATH


class QuestionAnalyser:
    def __init__(self):
        with open(FILM_PICKLE_PATH, 'rb') as f:
            self.film_dict = pickle.load(f)
        self.movie_titles = list(self.film_dict.keys())

        with open(HUMAN_PICKLE_PATH, 'rb') as f:
            self.human_dict = pickle.load(f)
        self.names = list(self.human_dict.keys())

        self.tokenizer = AutoTokenizer.from_pretrained("dslim/bert-large-NER")
        self.model = AutoModelForTokenClassification.from_pretrained("dslim/bert-large-NER")

    def get_movie_title(self, query):
        p_entities, m_entities = self.get_entities(query)
        print("People:", p_entities)
        print("Movies:", m_entities)
        fuzz_movie = self.do_fuzz_search(query, self.movie_titles)
        embed_movie = self.do_fuzz_search(''.join(m_entities), self.movie_titles)

        matched_names = self.do_fuzz_search(''.join(p_entities), self.names)
        alt_names = self.do_fuzz_search(query, self.names, fuzz.WRatio)
        if len(matched_names) == 0 and alt_names[0][1]>86:
            matched_names = alt_names

        if not fuzz_movie and not embed_movie:
            return [], matched_names
        elif not fuzz_movie:
            return [embed_movie[0][0]], matched_names
        elif not embed_movie:
            return [fuzz_movie[0][0]], matched_names
        else:
            return ([fuzz_movie[0][0]], matched_names) if fuzz_movie[0][1] > embed_movie[0][1] else (
            [embed_movie[0][0]], matched_names)

    def do_fuzz_search(self, entities, choices,scorer=fuzz.ratio):
        # Use fuzzywuzzy to find the closest match in your dictionary to the user query

        best_match = process.extract(entities, choices, scorer=scorer, processor=utils.default_process, limit=1)

        # best_match is a tuple containing the best matching movie title and a score
        # matching_movie_title, score = best_match
        matched_movies = []
        for movie in best_match:
            print("FUZZY SEARCH results:", movie)
            if int(movie[1]) > 70:
                matched_movies.append(movie)

        # 'the beautician and the beast' -> beauty and the beast
        # if 'the beautician and the beast' in matched_movies:
        for i in range(len(matched_movies)):
            if matched_movies[i] == "the beautician and the beast":
                matched_movies[i] = "beauty and the beast"
            elif matched_movies[i] == "eros":
                matched_movies[i] = "shoplifters"
            elif matched_movies[i] == "the bridge":
                matched_movies[i] = "the bridge on the river kwai"
        return matched_movies

    def get_entities(self, sentence):
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
