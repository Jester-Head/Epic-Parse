import scrapy


class WoWForumsItem(scrapy.Item):
    topic = scrapy.Field()
    forum_name = scrapy.Field()
    player_name = scrapy.Field()
    comment = scrapy.Field()
    likes = scrapy.Field()
    date = scrapy.Field()
