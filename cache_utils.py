from pymemcache.client.base import Client
import json


class Memcache:
    def __init__(self):
        self.client = Client(
            ('localhost', 11211), serializer=self.json_serializer, deserializer=self.json_deserializer)

    def json_serializer(self, key, value):
        # Serializer for the client of pymemcache.
        if type(value) == str:
            return value, 1
        return json.dumps(value), 2

    def json_deserializer(self, key, value, flags):
        # Deserializer for the client of pymemcache.
        try:
            if flags == 1:
                return value
            if flags == 2:
                return json.loads(value)
            raise Exception("Unknown serialization format")
        except Exception as e:
            self.logger.exception(str(e))

    def get_data_from_cache(self, key):
        return self.client.get(key)

    def dump_data_to_cache(self, key, value):
        self.client.set(key, value)

    def delete_from_cache(self, key):
        self.client.delete(key)
