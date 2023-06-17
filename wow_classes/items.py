import scrapy


class WowClassItem(scrapy.Item):
    topic = scrapy.Field()
    class_name = scrapy.Field()
    player_name = scrapy.Field()
    # comment = scrapy.Field()
    player_name = scrapy.Field()
    comment = scrapy.Field()
    likes = scrapy.Field()
    date = scrapy.Field()
    

class ClassMechanicsItem(scrapy.Item):
    class_name = scrapy.Field()
    spell_icon = scrapy.Field()
    ability = scrapy.Field()
    school = scrapy.Field()

class TweetItem(scrapy.Item):
    text = scrapy.Field()
    username = scrapy.Field()
    date = scrapy.Field()
