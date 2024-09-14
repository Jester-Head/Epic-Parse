import re
from itemloaders.processors import TakeFirst,MapCompose
from scrapy.loader import ItemLoader

class ForumItemLoader(ItemLoader):
    
    default_output_processor = TakeFirst()
    forum_name_in = MapCompose(lambda x: re.sub(r"\['|\']", "", x))