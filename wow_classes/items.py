import scrapy


class WowClassItem(scrapy.Item):
    topic = scrapy.Field()
    class_name = scrapy.Field()
    player_name = scrapy.Field()
    comment = scrapy.Field()
    likes = scrapy.Field()
    date = scrapy.Field()
