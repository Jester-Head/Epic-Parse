from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

class MongoDBConnection:
    def __init__(self, host='localhost', port=27017):
        self.host = host
        self.port = port
        self._client = None
        self._connect()

    def _connect(self):
        try:
            self._client = MongoClient(self.host, self.port)
            # Trigger a server selection to verify connection
            self._client.server_info()
        except ConnectionFailure:
            print("Failed to connect to MongoDB server")
            self._client = None

    def get_collection(self, db_name, collection_name):
        """
        Return a collection object to perform operations.
        
        :param db_name: Name of the database.
        :param collection_name: Name of the collection within the database.
        :return: Collection object or None.
        """
        if self._client:
            db = self._client[db_name]
            return db[collection_name]
        print("Connection not established. Can't fetch collection.")
        return None

    def close(self):
        if self._client:
            self._client.close()



