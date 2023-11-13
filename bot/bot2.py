import time
import uuid
from typing import List

from bot.util.recommender import Recommender
from config.conf import BOT_NAME, BOT_PASS, BOT_PATH, BOT_BASE_PATH
from speakeasypy import Speakeasy, Chatroom
from util.cache import Cache
from util.graph import Graph
from util.llm import LLM
from util.question_analyser import QuestionAnalyser

import sys
sys.path.append(BOT_PATH)
sys.path.append(BOT_BASE_PATH)

class Agent:
    DISPLAY_FORMAT_DATETIME: str = "%H:%M:%S, %d-%m-%Y"
    SPEAKEASY_HOST_URL: str = 'https://speakeasy.ifi.uzh.ch'
    LISTEN_FREQUENCY_IN_SECS = 2

    def __init__(self, username: str, password: str):
        self.username: str = username
        self.speakeasy = Speakeasy(host=Agent.SPEAKEASY_HOST_URL, username=username, password=password)
        self.speakeasy.login()  # This framework will help you log out automatically when the program terminates.
        # Use the best dataset for open questions with no underlaying dataset
        self.llm = LLM(heavy_mode=True)
        self.graph = Graph()
        self.analyser = QuestionAnalyser()
        self.cacher = Cache()
        self.current_user = str(uuid.uuid4())[:8]
        self.recommender = Recommender()
        print("---READY FOR OPERATION---")

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

                    if message.message in self.cacher.cache:
                        print("Cache Hit!")
                        response =  self.cacher.cache[message.message]
                    else:
                        if "{" in message.message and "}" in message.message:
                            trimmed_message = message.message.strip()
                            self.recommender.submit_entry(self.current_user, trimmed_message)
                            recommendations = '_'.join(self.recommender.get_neighbors())
                            self._repond(message, recommendations)
                        elif "best recommendations" in message.message:
                            self._repond(message, "what is your rating ? respect this format {'Inception': 5}")
                        else:
                            movie_titles = self.analyser.get_movie_title(message.message)
                            movie_data = self.graph.get_film_info(movie_titles)
                            if movie_data:
                                response = self.llm.ask_about_movies(question=message.message, data=movie_data)
                            else:
                                response = self.llm.ask_no_data(message.message)
                            if response != "error":
                                self.cacher.cache_message(message.message, response)
                            self._repond(message, response, room)

                # Retrieve reactions from this chat room.
                # If only_new=True, it filters out reactions that have already been marked as processed.
                for reaction in room.get_reactions(only_new=True):
                    print(
                        f"\t- Chatroom {room.room_id} "
                        f"- new reaction #{reaction.message_ordinal}: '{reaction.type}' "
                        f"- {self.get_time()}")
                    room.mark_as_processed(reaction)

            time.sleep(Agent.LISTEN_FREQUENCY_IN_SECS)

    def _repond(self, message, response, room):
        print("POSTING RESPONE:", response)
        # Send a message to the corresponding chat room using the post_messages method of the room object.
        room.post_messages(response)
        # Mark the message as processed, so it will be filtered out when retrieving new messages.
        room.mark_as_processed(message)

    @staticmethod
    def get_time():
        return time.strftime(Agent.DISPLAY_FORMAT_DATETIME, time.localtime())


if __name__ == '__main__':
    demo_bot = Agent(BOT_NAME, BOT_PASS)
    demo_bot.listen()

