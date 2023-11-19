import pickle

from collections import defaultdict

from config.conf import HIGH_PRIO_PICKLE_PATH, FILM_PICKLE_PATH


class Graph:
    def __init__(self):
        print("--STARTING TO LOAD GRAPH--")
        with open(HIGH_PRIO_PICKLE_PATH, 'rb') as f:
            self.graph = pickle.load(f)
            print("--LOADED GRAPH--")
        with open(FILM_PICKLE_PATH, 'rb') as f:
            self.movie_dict = pickle.load(f)
            print("--LOADED MOVIE DICT--")

    def get_film_info(self, matched_movies):
        query_template = """PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX wd: <http://www.wikidata.org/entity/>
            PREFIX wdt: <http://www.wikidata.org/prop/direct/>
            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
            
            SELECT ?predicate ?predicateLabel ?object ?objectLabel WHERE {{
              {0} ?predicate ?object .
              FILTER(?predicate NOT IN (wdt:P5021, wdt:P8889, wdt:P8874, wdt:P5970, wdt:P3650, wdt:P3306, wdt:P2747,wdt:P2629,wdt:P6658, wdt:P3216, wdt:P3216, wdt:P2758, wdt:P3402, wdt:P2756, wdt:P4437, wdt:P3428, wdt:P2684, wdt:P2363, wdt:P2637, wdt:P3834))
              OPTIONAL {{ ?predicate rdfs:label ?predicateLabel . FILTER(LANG(?predicateLabel) = "en") }}
              OPTIONAL {{ ?object rdfs:label ?objectLabel . FILTER(LANG(?objectLabel) = "en") }}
            }}
            """
        reduced_info_template = """
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX wd: <http://www.wikidata.org/entity/>
                PREFIX wdt: <http://www.wikidata.org/prop/direct/>
                PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
            
                SELECT ?movie ?movieLabel ?predicateLabel ?object ?objectLabel WHERE {{
                  VALUES ?movie {{ {0} }} 
                  ?movie ?predicate ?object .
                  FILTER(?predicate IN (
                      wdt:P31,   # instance of
                      wdt:P57,   # director
                      wdt:P162,  # producer
                      wdt:P364,  # original language
                      wdt:P272,  # production company
                      wdt:P58,   # screenwriter
                      wdt:P166,  # award received
                      wdt:P2047, # duration
                      wdt:P577 # release date
                  ))
                  OPTIONAL {{ ?predicate rdfs:label ?predicateLabel . FILTER(LANG(?predicateLabel) = "en") }}
                  OPTIONAL {{ ?object rdfs:label ?objectLabel . FILTER(LANG(?objectLabel) = "en") }}
                  OPTIONAL {{ ?movie rdfs:label ?movieLabel . FILTER(LANG(?movieLabel) = "en") }}
                }}
                ORDER BY ?movie
            """

        data = []
        for movie in matched_movies:
            entity = self.movie_dict[movie]
            if isinstance(entity, list):
                query = reduced_info_template.format(' '.join(entity))
                result = self.graph.query(query)

                # Convert to dictionary
                def add_value(entity_key, key, value):
                    if entity_key not in film_info:
                        film_info[entity_key] = defaultdict(list)
                    film_info[entity_key][key].append(value)

                film_info = {}

                for entity_key, movie_label, label, obj, value in result:
                    if value is None:
                        add_value(str(entity_key.rsplit('/', 1)[-1]) + str(movie_label), str(label), str(obj))
                    add_value(str(entity_key.rsplit('/', 1)[-1]) + str(movie_label), str(label), str(value))
            else:
                query = query_template.format(entity)
                result = self.graph.query(query)

                def add_value(key, value):
                    film_info[key].append(value)

                film_info = defaultdict(list)
                for row in result:
                    if row[1] is not None and row[3] is not None:
                        add_value(str(row[1]), str(row[3]))
                    elif row[1] is not None and row[2] is not None:
                        add_value(str(row[1]), str(row[2]))
                    elif row[1] is None:
                        add_value("tag", str(row[2]))

                data.append(film_info)
        return data
