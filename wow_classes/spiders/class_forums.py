import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from wow_classes.items import WowClassItem


class WoWClassForums(CrawlSpider):
    """
    A Scrapy spider that crawls the World of Warcraft forums and extracts information about class-specific discussions.
    """
    name = 'wow_classes'
    custom_settings = {
        'ITEM_PIPELINES': {
            'wow_classes.pipelines.FourmsPipeline': 300,
        }
    }

    allowed_domains = ['us.forums.blizzard.com']
    start_urls = ['https://us.forums.blizzard.com/en/wow/c/classes/death-knight/175/l/top?period=quarterly', 'https://us.forums.blizzard.com/en/wow/c/classes/demon-hunter/176/l/top?period=quarterly', 'https://us.forums.blizzard.com/en/wow/c/classes/druid/177/l/top?period=quarterly', 'https://us.forums.blizzard.com/en/wow/c/classes/evoker/275/l/top?period=quarterly',
                  'https://us.forums.blizzard.com/en/wow/c/classes/hunter/178/l/top?period=quarterly', 'https://us.forums.blizzard.com/en/wow/c/classes/mage/179/l/top?period=quarterly', 'https://us.forums.blizzard.com/en/wow/c/classes/monk/180/l/top?period=quarterly', 'https://us.forums.blizzard.com/en/wow/c/classes/paladin/181/l/top?period=quarterly',
                  'https://us.forums.blizzard.com/en/wow/c/classes/priest/182/l/top?period=quarterly', 'https://us.forums.blizzard.com/en/wow/c/classes/rogue/183/l/top?period=quarterly', 'https://us.forums.blizzard.com/en/wow/c/classes/shaman/184/l/top?period=quarterly', 'https://us.forums.blizzard.com/en/wow/c/classes/warlock/185/l/top?period=quarterly',
                  'https://us.forums.blizzard.com/en/wow/c/classes/warrior/186/l/top?period=quarterly']

    rules = (

        Rule(LinkExtractor(allow=('^https://us.forums.blizzard.com/en/wow/c/'),
             deny=('^https://worldofwarcraft.com/en-us/character/', '^https://us.forums.blizzard.com/en/wow/u/'))),

        Rule(LinkExtractor(allow=(
            '^https://us.forums.blizzard.com/en/wow/t/', )), callback='parse_thread'),
    )

    def parse(self, response):
        """
        Extract links from the page and follow them to extract thread data.

        Parameters:
            response (Response): The response object containing the page to be parsed.

        Yields:
            Request: A request for the next page of data to be parsed.
        """
        links = response.xpath('//a/@href').extract()
        for link in links:
            absolute_url = response.urljoin(link)
            yield scrapy.Request(absolute_url, callback=self.parse_thread, dont_filter=False, encoding='utf-8')

    def parse_thread(self, response):
        """
        Extract data from a forum thread page and create an item for it.

        Parameters:
            response (Response): The response object containing the page to be parsed.

        Yields:
            WowClassItem: An item containing the data extracted from the page.
        """

        comments = response.xpath('//div[@class="post"]')

        title = response.xpath('//h1/a/text()').extract_first()

        content = comments.xpath('//div[@class="post"]/p/text()').extract()
        date_published = comments.xpath(
            '//div[1]/div/div/span/time/@datetime').extract()
        likes = comments.xpath(
            '//div[@itemprop="interactionStatistic"]/span/text()').extract()
        class_name = response.xpath(
            '//*[@id="topic-title"]/div/span[2]/a/span[2]/span/text()').extract()
        
        player_name = response.xpath('.//span[@class = "creator"]/a/span/text()').extract()
        # player_name = response.xpath('//a/@data-user-card').extract()

        comments = list(zip(player_name,content, likes, date_published,))

        for comment in comments:
            item = WowClassItem()
            item['topic'] = title
            item['class_name'] = class_name[0]
            item['comment'] = {
                'player_name': comment[0],
                'content': comment[1],
                'likes': comment[2],
                'date': comment[3]
            }
            yield item
