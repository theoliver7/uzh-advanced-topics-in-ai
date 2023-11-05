from collections import OrderedDict


class Cache:
    def __init__(self, cache_size=50):
        self.cache = OrderedDict()
        self.cache_size = cache_size

    def cache_message(self, message, response):
        if len(self.cache) >= self.cache_size:
            # Remove the oldest item from the cache if the cache is full
            self.cache.popitem(last=False)
        # Add the new message and response to the cache
        self.cache[message] = response
