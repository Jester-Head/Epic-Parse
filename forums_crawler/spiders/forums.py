import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from forums_crawler.items import WoWForumsItem


class WowForumsCrawler(CrawlSpider):
    """
    A Scrapy spider that crawls the World of Warcraft forums and extracts information about general discussions,
    using Playwright for JavaScript rendering to handle dynamically loaded content.
    
    Playwright is used to wait for key elements to load before extracting data, which is crucial for pages that use 
    JavaScript to render content after the page is initially loaded. This spider will follow links and extract data 
    such as comments, forum names, post titles, and other metadata.
    """
    name = 'forums'

    custom_settings = {
        'ITEM_PIPELINES': {
            'forums_crawler.pipelines.WoWForumsPipeline': 300,  # Correct path to the pipeline class
        },
        'DOWNLOAD_HANDLERS': {
            'http': 'scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler',
            'https': 'scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler',
        },
        'TWISTED_REACTOR': 'twisted.internet.asyncioreactor.AsyncioSelectorReactor',  # Use Asyncio reactor for Playwright compatibility
    }

    allowed_domains = ['us.forums.blizzard.com']

    start_urls = [
        'https://us.forums.blizzard.com/en/wow/c/community/general-discussion/171','https://us.forums.blizzard.com/en/wow/g/blizzard-tracker/activity/topics/','https://us.forums.blizzard.com/en/wow/c/classes/'
    ]

    # Define rules to follow links within the allowed domains
    rules = (
        Rule(
            LinkExtractor(
                allow=(
                    'https://us.forums.blizzard.com/en/wow/c/',  # General discussions
                    'https://us.forums.blizzard.com/en/wow/t/',  # Threads within the forums
                    'https://us.forums.blizzard.com/en/wow/c/classes/',  # Class discussions
                    'https://us.forums.blizzard.com/en/wow/g/blizzard-tracker/activity/topics/'  # Blizzard tracker activity
                ),
                deny=(
                    'https://worldofwarcraft.com/en-us/character/',  # Avoid user profile links
                    'https://us.forums.blizzard.com/en/wow/u/',  # Avoid user pages
                    'https://us.forums.blizzard.com/en/wow/c/recruitment/',  # Avoid recruitment category
                    'https://us.forums.blizzard.com/en/wow/c/off-topic/',  # Avoid off-topic category
                    'https://us.forums.blizzard.com/en/wow/c/wow-classic/',  # Avoid WoW Classic category
                    'https://us.forums.blizzard.com/en/wow/c/wow-classic/classic-discussion/',  # Avoid Classic discussion category
                    'https://us.forums.blizzard.com/en/wow/c/in-development/cataclysm-classic/',  # Avoid Cataclysm Classic category
                    'https://us.forums.blizzard.com/en/wow/c/in-development/season-of-discovery/',  # Avoid Season of Discovery category
                    'div.filtered-realms.classic',  # Avoid filtered realms section
                    'h3'  # Avoid certain header elements
                )
            ),
            callback='parse_thread',  # Parse the thread once a valid link is found
            process_request='use_playwright',  # Use Playwright to render JavaScript content
            follow=True
        ),
        Rule(
            LinkExtractor(restrict_xpaths='//a[@rel="next"]'),  # Follow "next" button for pagination
            follow=True
        )
    )

    def use_playwright(self, request,response):
            """
            Modify the request to use Playwright for JavaScript-rendered pages.

            Playwright waits for the specified selector to be present before continuing with the scraping.
            This is useful for pages that load content dynamically via JavaScript.

            Parameters:
                request (Request): The Scrapy request object.

            Returns:
                Request: The modified request to use Playwright for rendering JavaScript.
            """
            request.meta["playwright"] = True
            return request


    def parse_thread(self, response):
        """
        Extract data from a forum thread page and create an item for each comment.

        The method processes the page and extracts various elements such as the title of the thread,
        the content of the comments, the published date, the number of likes for each comment, and the 
        forum name where the post is located. Each comment is then yielded as an item.

        Parameters:
            response (Response): The response object containing the page to be parsed.

        Yields:
            WoWForumsItem: An item containing the extracted data from the forum post.
        """
        # Extract all the posts from the page
        comments = response.xpath('//div[@class="post"]')

        # Extract the thread title
        title = response.xpath('//h1/a/text()').extract_first()

        # Extract the content of each comment
        content = comments.xpath('//div[@class="post"]/p/text()').extract()

        # Extract the published date of each comment
        date_published = comments.xpath('//span[@class="crawler-post-infos"]/time[@itemprop="datePublished"]/@datetime').extract()

        # Extract the number of likes for each comment
        likes = comments.xpath('//span[contains(text(),"Likes")]/text()').extract()

        # Extract the forum name where the thread is located
        forum_name = response.xpath('//*[@id="topic-title"]/div/span[2]/a/span[2]/span/text()').extract()

        # Extract the name of the player who made each comment
        player_name = response.xpath('//span[@class="creator" and @itemprop="author"]/a/span[@itemprop="name"]/text()').extract()

        # Zip the player names, content, likes, and dates together for each comment
        comments = list(zip(player_name, content, likes, date_published))

        # Yield each comment as an item
        for comment in comments:
            item = WoWForumsItem()
            item['topic'] = title
            item['forum_name'] = forum_name[0] if forum_name else 'Unknown'
            item['comment'] = {
                'player_name': comment[0],
                'content': comment[1],
                'likes': comment[2],
                'date': comment[3]
            }
            yield item
