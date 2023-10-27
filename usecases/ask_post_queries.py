# set up steps
# 1. have a conf.py file in config package
# 2. put the database files in the good place usecases/files cf README_FILES.md
# 3. USE QUERIES WHILE COMMUNICATING WITH THE BOT LIKE IN A CODE EXAMPLE
'''
            prefix wdt: <http://www.wikidata.org/prop/direct/>
            prefix wd: <http://www.wikidata.org/entity/>

            SELECT ?obj ?lbl WHERE {
                ?ent rdfs:label "Jean Van Hamme"@en .
                ?ent wdt:P106 ?obj .
                ?obj rdfs:label ?lbl .
            }
'''
import os
import pickle
# 1 - OPTIONAL - start time when load graph database
# 2 - PROVIDED REQUESTS DO NOT WORK (even using the assignmeent.ipynb notebook) - ASK TO TEACHER / COLLEAGUES ?

# rdflib in order to request a graph database using SPARQL
# and do calls (queries) to this database in the code

import time
from typing import List

import rdflib

from config.conf import BOT_NAME, BOT_PASS, FILES_PATH, DEFAULT_MODE
from speakeasypy import Speakeasy, Chatroom
from transformers import pipeline, set_seed

DEFAULT_HOST_URL = 'https://speakeasy.ifi.uzh.ch'
listen_freq = 2

# --> ***DAVID*** INTEGRATE GRAPH OBJECT AND ITS DEPENDENCIES
WD = rdflib.Namespace('http://www.wikidata.org/entity/')
WDT = rdflib.Namespace('http://www.wikidata.org/prop/direct/')
DDIS = rdflib.Namespace('http://ddis.ch/atai/')
RDFS = rdflib.namespace.RDFS
SCHEMA = rdflib.Namespace('http://schema.org/')

# database files, in order to improve bot start time (1min45... on my computer),
# we can try to serialize (write a binary file) the graph object,
# and deserialize it (read a binary file and load it in memory)
import os

serialized_path= f'{FILES_PATH}ddis-movie-graph.nt.pickle'

if not DEFAULT_MODE == "TEXT_GENERATION":
    if not os.path.exists(serialized_path):
        print("parsing graph")
        graph = rdflib.Graph().parse(f'{FILES_PATH}ddis-movie-graph.nt', format='turtle')
        with open(serialized_path, "wb") as f:
            pickle.dump(graph, f)
    else:
        with open(serialized_path, "rb") as f:
            print("loading graph")
            graph = pickle.load(f)

# entity_emb = np.load(f'{FILES_PATH}entity_embeds.npy')
# relation_emb = np.load(f'{FILES_PATH}relation_embeds.npy')
# relationships
#triples = {(s, p, o) for s, p, o in graph.triples((None, None, None)) if isinstance(o, rdflib.term.URIRef)}


# ***DAVID*** INTEGRATE GRAPH OBJECT AND ITS DEPENDENCIES <--


class Agent:
    QUERY_MODE: str = "QUERY"
    TEXT_GENERATION_MODE: str = "TEXT_GENERATION"

    def __init__(self, username, password, mode):
        self.username = username
        # --> ***DAVID*** - Initialize the Speakeasy Python framework and login.
        self.speakeasy = Speakeasy(host=DEFAULT_HOST_URL, username=username, password=password)
        self.speakeasy.login()  # This framework will help you log out automatically when the program terminates.
        # ***DAVID*** - Initialize the Speakeasy Python framework and login. <--
        # --> ***DAVID*** - Add mode in order to handle multi response type
        self.mode = mode
        #self.generation_pipeline = pipeline("text-generation", model='gpt2')
        self.generation_pipeline = pipeline("text-generation", model='EleutherAI/gpt-neo-2.7B')
        # <--

    # --> ***DAVID*** add method to query the text generation pipeline from the agent
    def query_text_generation_pipeline(self, query_message: str):
        #generated_text = self.generation_pipeline(text_inputs=query_message, max_new_tokens=200)
        generated_text = self.generation_pipeline(query_message, max_length=400, do_sample=True, temperature=0.9)

        print("***DEBUG TEXT GENERATION***")
        print(generated_text)
        print(generated_text[0]['generated_text'])
        print("***DEBUG TEXT GENERATION***")

        return generated_text[0]['generated_text']
    # <-- ***DAVID*** add method to query the text generation pipeline from the agent

    # --> ***DAVID*** add method to query the graph object from the agent
    def query_graphql(self, query_message: str):
        # exemple of working query on td example
        '''
            prefix wdt: <http://www.wikidata.org/prop/direct/>
            prefix wd: <http://www.wikidata.org/entity/>

            SELECT ?obj ?lbl WHERE {
                ?ent rdfs:label "Jean Van Hamme"@en .
                ?ent wdt:P106 ?obj .
                ?obj rdfs:label ?lbl .
            }
        '''
        # result formatted in a set
        query_result = set(graph.query(query_message))
        # display in beautiful mode
        bot_result = list(query_result)[0][0]

        # display only in bot console on your computer
        print(bot_result)

        return bot_result

    # ***DAVID*** add method to query the graph object from the agent <--

    def listen(self):
        while True:
            # only check active chatrooms (i.e., remaining_time > 0) if active=True.
            rooms: List[Chatroom] = self.speakeasy.get_rooms(active=True)
            for room in rooms:
                if not room.initiated:
                    # send a welcome message if room is not initiated
                    room.post_messages(f'Hello! This is a welcome message from {room.my_alias}.')
                    room.initiated = True
                # Retrieve messages from this chat room.
                # If only_partner=True, it filters out messages sent by the current bot.
                # If only_new=True, it filters out messages that have already been marked as processed.
                for message in room.get_messages(only_partner=True, only_new=True):
                    print(
                        f"\t- Chatroom {room.room_id} "
                        f"- new message #{message.ordinal}: '{message.message}' "
                        f"- {self.get_time()}")

                    # Implement your agent here #

                    # --> ***DAVID*** ADD RETURN FROM BOT
                    try:
                        # ask bot response using graph db
                        bot_resp = ''
                        if self.mode == Agent.QUERY_MODE:
                            bot_resp = self.query_graphql(message.message)
                        else:
                            bot_resp = self.query_text_generation_pipeline(message.message)

                        # bot send the result in the chat (web interface : https://speakeasy.ifi.uzh.ch/chat...)
                        room.post_messages(f"{bot_resp}")
                    except Exception as e:
                        print(e)
                    # ***DAVID*** ADD RETURN FROM BOT <--

                    # Mark the message as processed, so it will be filtered out when retrieving new messages.
                    room.mark_as_processed(message)

                # Retrieve reactions from this chat room.
                # If only_new=True, it filters out reactions that have already been marked as processed.
                for reaction in room.get_reactions(only_new=True):
                    print(
                        f"\t- Chatroom {room.room_id} "
                        f"- new reaction #{reaction.message_ordinal}: '{reaction.type}' "
                        f"- {self.get_time()}")

                    # Implement your agent here #

                    room.post_messages(f"Received your reaction: '{reaction.type}' ")
                    room.mark_as_processed(reaction)

            time.sleep(listen_freq)

    @staticmethod
    def get_time():
        return time.strftime("%H:%M:%S, %d-%m-%Y", time.localtime())


if __name__ == '__main__':
    demo_bot = Agent(BOT_NAME, BOT_PASS, Agent.TEXT_GENERATION_MODE)
    demo_bot.listen()
