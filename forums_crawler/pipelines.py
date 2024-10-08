import pymongo
from itemadapter import ItemAdapter
from pymongo import errors


class WoWForumsPipeline:
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
            FourmsPipeline: An instance of FourmsPipeline initialized with settings from the crawler.
        """
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DATABASE", "wow_test"),
            mongo_coll=crawler.settings.get(
                "MONGO_COLL_FORUMS", "forums"),
        )

    def open_spider(self, spider):
        """
        Establish a connection to MongoDB when the spider is opened and set up the necessary indexes.

        Parameters:
            spider (Spider): The Scrapy Spider instance that is being run.
        """
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.collection = self.db[self.mongo_coll]

        try:
            # Create a unique compound index
            self.collection.create_index([
                ("topic", 1),
                ("forum_name", 1),
                ("comment", 1),
                ("player_name", 1),
                ("content", 1),
                ("likes", 1),
                ("date", 1),
            ], unique=True)
        except errors.OperationFailure as e:
            spider.logger.error(f"Error creating index: {e}")

    def close_spider(self, spider):
        """
        Close the connection to MongoDB when the spider is closed.

        Parameters:
            spider (Spider): The Scrapy Spider instance that has finished running.
        """
        self.client.close()

    def process_item(self, item, spider):
        """
        Process an item by inserting it into the MongoDB collection. If a duplicate item is detected, 
        it's logged and skipped.

        Parameters:
            item (Item): The item scraped by the spider.
            spider (Spider): The Scrapy Spider instance that scraped the item.

        Returns:
            Item: The processed item.
        """
        try:
            item_dict = ItemAdapter(item).asdict()
            self.collection.insert_one(item_dict)
        except errors.DuplicateKeyError:
            item_dict = ItemAdapter(item).asdict()
            spider.logger.info("Duplicate item found: %s", item_dict)
            pass
        return item
