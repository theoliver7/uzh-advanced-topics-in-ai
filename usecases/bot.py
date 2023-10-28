from usecases.util.cache import Cache
from usecases.util.graph import Graph
from usecases.util.llm import LLM
from explorations.question_analyser import QuestionAnalyser

import os
import pickle

import time
from typing import List

import rdflib

from config.conf import BOT_NAME, BOT_PASS, FILES_PATH, DEFAULT_MODE
from speakeasypy import Speakeasy, Chatroom
from transformers import pipeline

WD = rdflib.Namespace('http://www.wikidata.org/entity/')
WDT = rdflib.Namespace('http://www.wikidata.org/prop/direct/')
DDIS = rdflib.Namespace('http://ddis.ch/atai/')
RDFS = rdflib.namespace.RDFS
SCHEMA = rdflib.Namespace('http://schema.org/')

SERIALIZED_COMPLETE_PATH = f'{FILES_PATH}ddis-movie-graph.nt.pickle'

if not DEFAULT_MODE == "TEXT_GENERATION":
    if not os.path.exists(SERIALIZED_COMPLETE_PATH):
        print("parsing graph")
        graph = rdflib.Graph().parse(f'{FILES_PATH}ddis-movie-graph.nt', format='turtle')
        with open(SERIALIZED_COMPLETE_PATH, "wb") as f:
            pickle.dump(graph, f)
    else:
        with open(SERIALIZED_COMPLETE_PATH, "rb") as f:
            print("loading graph")
            graph = pickle.load(f)


class Agent:
    DISPLAY_FORMAT_DATETIME: str = "%H:%M:%S, %d-%m-%Y"
    SPEAKEASY_HOST_URL: str = 'https://speakeasy.ifi.uzh.ch'
    LISTEN_FREQUENCY_IN_SECS = 2
    QUERY_MODE: str = "QUERY"
    TEXT_GENERATION_MODE: str = "TEXT_GENERATION"
    TEXT_GENERATION_RESPONSE_LENGTH = 400
    SET_MODE: str = "SET_MODE"

    def __init__(self, username: str, password: str):
        self.username: str = username
        self.speakeasy = Speakeasy(host=Agent.SPEAKEASY_HOST_URL, username=username, password=password)
        self.speakeasy.login()  # This framework will help you log out automatically when the program terminates.
        self.llm = LLM()
        self.graph = Graph()
        self.analyser = QuestionAnalyser()
        self.cacher = Cache()
        self.mode = Agent.QUERY_MODE
        self.generation_pipeline = pipeline("text-generation", model='gpt2')
        #self.generation_pipeline = pipeline("text-generation", model='EleutherAI/gpt-neo-2.7B')
        #self.generation_pipeline = pipeline("text-generation", model='EleutherAI/gpt-neo-1.3B')
        print("---READY FOR OPERATION---")

    def _query_text_generation_pipeline(self, query_message: str) -> str:
        generated_text = self.generation_pipeline(query_message, max_length=Agent.TEXT_GENERATION_RESPONSE_LENGTH, do_sample=True, temperature=0.9)

        print("***DEBUG TEXT GENERATION***")
        print(generated_text)

        return generated_text[0]['generated_text']

    def _set_response_mode_on_ask(self, message):
        if message.message == Agent.SET_MODE:
            if self.mode == Agent.QUERY_MODE:
                self.mode = Agent.TEXT_GENERATION_MODE
            else:
                self.mode = Agent.QUERY_MODE
            print(f'SET MODE to {self.mode}')
        else:
            message.message = ''
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

                    self._set_response_mode_on_ask(message)

                    if message.message in self.cacher.cache:
                        print("Cache Hit!")
                        response = self.cacher.cache[message.message]
                    else:
                        if self.mode == Agent.QUERY_MODE:
                            movie_titles = self.analyser.get_movie_title(message.message)
                            movie_data = self.graph.get_film_info(movie_titles)
                            if movie_data:
                                response = self.llm.ask_about_movies(question=message.message, data=movie_data)
                            else:
                                response = self.llm.ask_no_data(message.message)
                        else:
                            response = self._query_text_generation_pipeline(message.message)

                        self.cacher.cache_message(message.message, response)
                    print(f"POSTING RESPONE: {message}")
                    # Send a message to the corresponding chat room using the post_messages method of the room object.
                    room.post_messages(response)
                    # Mark the message as processed, so it will be filtered out when retrieving new messages.
                    room.mark_as_processed(message)

                # Retrieve reactions from this chat room.
                # If only_new=True, it filters out reactions that have already been marked as processed.
                for reaction in room.get_reactions(only_new=True):
                    print(
                        f"\t- Chatroom {room.room_id} "
                        f"- new reaction #{reaction.message_ordinal}: '{reaction.type}' "
                        f"- {self.get_time()}")
                    room.mark_as_processed(reaction)

            time.sleep(Agent.LISTEN_FREQUENCY_IN_SECS)

    @staticmethod
    def get_time():
        return time.strftime(Agent.DISPLAY_FORMAT_DATETIME, time.localtime())


if __name__ == '__main__':
    demo_bot = Agent(BOT_NAME, BOT_PASS)
    demo_bot.listen()

