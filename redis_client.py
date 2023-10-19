import redis, json
from redis.exceptions import  ConnectionError

class RedisClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.redis = redis.Redis(host=self.host, port=self.port)

    def set(self, key, value):
        try:
            self.redis.set(key, json.dumps(value))
        except ConnectionError:
            print("Connection Error Redis")

    def get(self, key):
        try:
            return json.loads(self.redis.get(key))
        except ConnectionError:
            print("Connection Error Redis")

    def delete(self, key):
        try:
            self.redis.delete(key)
        except ConnectionError:
            print("Connection Error Redis")

    def exists(self, key):
        try:
            return self.redis.exists(key)
        except ConnectionError:
            print("Connection Error Redis")

    def keys(self, pattern):  # pattern = "*"
        try:
            return self.redis.keys(pattern)
        except ConnectionError:
            print("Connection Error Redis")

    def flush(self):
        try:
            self.redis.flushall()
        except ConnectionError:
            print("Connection Error Redis")