import pymongo
from itemadapter import ItemAdapter


class FourmsPipeline:
    def __init__(self, mongo_uri, mongo_db, mongo_coll):
        """
        Initialize the Forums pipeline with the necessary settings for connecting to MongoDB.

        Parameters:
            mongo_uri (str): URI for connecting to MongoDB.
            mongo_db (str): Name of the database to store the data in.
            mongo_coll (str): Name of the collection to store the data in.
        """
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_coll = mongo_coll

    @classmethod
    def from_crawler(cls, crawler):
        """
        Obtain the necessary settings for the pipeline from the Scrapy settings.

        Parameters:
            crawler (Crawler): The Scrapy Crawler instance.

        Returns:
            FourmsPipeline: The initialized pipeline instance.
        """
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DATABASE", "wow_test"),
            mongo_coll=crawler.settings.get(
                "MONGO_COLL_FORUMS", "class_forums"),
        )

    def open_spider(self, spider):
        """Connect to MongoDB when the spider is opened."""
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.collection = self.db[self.mongo_coll]

    def close_spider(self, spider):
        """Close the connection to MongoDB when the spider is closed."""
        self.client.close()

    def process_item(self, item, spider):
        """Process an item by inserting it into the MongoDB collection."""
        item_dict = ItemAdapter(item).asdict()
        self.collection.insert_one(item_dict)
        return item
