import time

cache = {}
CACHE_TTL = 60  # segundos

def get_cache(key):
    if key in cache:
        valor, timestamp = cache[key]
        if time.time() - timestamp < CACHE_TTL:
            return valor
    return None

def set_cache(key, value):
    cache[key] = (value, time.time())
