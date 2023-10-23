import pickle

from collections import defaultdict


class Graph:
    def __init__(self):
        print("hi")
        with open('../dataset/graph-high-prio.pickle', 'rb') as f:
            self.graph = pickle.load(f)
            print("--LOADED GRAPH--")
        with open('../dataset/film_dict.pickle', 'rb') as f:
            self.movie_dict = pickle.load(f)
            print("--LOADED MOVIE DICT--")

    def get_film_info(self,matched_movies):
        query_template = """PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX wd: <http://www.wikidata.org/entity/>
        PREFIX wdt: <http://www.wikidata.org/prop/direct/>
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

        SELECT ?predicate ?predicateLabel ?object ?objectLabel WHERE {{
          wd:{0} ?predicate ?object .
          OPTIONAL {{ ?predicate rdfs:label ?predicateLabel . FILTER(LANG(?predicateLabel) = "en") }}
          OPTIONAL {{ ?object rdfs:label ?objectLabel . FILTER(LANG(?objectLabel) = "en") }}
        }}
        """

        data = []
        for movie in matched_movies:
            uri = self.movie_dict[movie]
            entity = uri.rsplit('/', 1)[-1]
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
            print(data)
        return data