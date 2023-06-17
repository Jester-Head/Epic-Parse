from pymongo import MongoClient


class MongoDBConnection:
    def __init__(self, host='localhost', port=27017):
        self.host = host
        self.port = port
        self.client = None

    def __enter__(self):
        self.client = MongoClient(host=self.host, port=self.port)
        return self.client

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()
