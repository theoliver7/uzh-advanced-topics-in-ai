import sys

from conf import BOT_BOT_PATH, BOT_BASE_PATH, BOT_NAME, BOT_PASS

sys.path.insert(1, BOT_BASE_PATH)
sys.path.insert(0, BOT_BOT_PATH)
sys.path.insert(2, BOT_BASE_PATH)

from bot import Bot

import time
from typing import List

from speakeasypy import Speakeasy, Chatroom
import speakeasypy
from util.cache import Cache


class Agent:
    DISPLAY_FORMAT_DATETIME: str = "%H:%M:%S, %d-%m-%Y"
    SPEAKEASY_HOST_URL: str = 'https://speakeasy.ifi.uzh.ch'
    LISTEN_FREQUENCY_IN_SECS = 2

    def __init__(self, username: str, password: str):
        self.username: str = username
        self.speakeasy = Speakeasy(host=Agent.SPEAKEASY_HOST_URL, username=username, password=password)
        self.speakeasy.login()  # This framework will help you log out automatically when the program terminates.
        self.bot = Bot()
        self.cacher = Cache()
        print("---READY FOR OPERATION---")

    def listen(self):
        while True:
            # only check active chatrooms (i.e., remaining_time > 0) if active=True.
            rooms: List[Chatroom] = self.speakeasy.get_rooms(active=True)
            for room in rooms:
                if not room.initiated:
                    # send a welcome message if room is not initiated
                    room.post_messages(f'Hello! This is {room.my_alias} your helpful movie chatbot. Ask away!.')
                    room.initiated = True
                # Retrieve messages from this chat room.
                # If only_partner=True, it filters out messages sent by the current bot.
                # If only_new=True, it filters out messages that have already been marked as processed.
                for message in room.get_messages(only_partner=True, only_new=True):
                    print(
                        f"\t- Chatroom {room.room_id} "
                        f"- new message #{message.ordinal}: '{message.message}' "
                        f"- {self.get_time()}")
                    hit, cache_value = self.cacher.exist(message.message)
                    if hit:
                        print("Cache Hit!")
                        response = cache_value
                    else:
                        response = self.bot.ask(message.message)
                        if response != "Something went wrong :(. Please try again!":
                            self.cacher.cache_message(message.message, response)
                    print("POSTING RESPONE:", response)

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
