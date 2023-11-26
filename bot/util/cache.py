import pickle
from collections import OrderedDict

from config.conf import CACHE_PICKLE_PATH


class Cache:
    def __init__(self, cache_size=100):
        self.cache = OrderedDict()
        self.cache_size = cache_size
        with open(CACHE_PICKLE_PATH, 'rb') as f:
            self.cache = pickle.load(f)

    def cache_message(self, message, response):
        if len(self.cache) >= self.cache_size:
            # Remove the oldest item from the cache if the cache is full
            self.cache.popitem(last=False)
        # Add the new message and response to the cache
        self.cache[message] = response

    def exist(self, query):
        for key, value in self.cache.items():
            if query.lower() in key.lower():
                return True,value
        return False,""
