import scrapy


class TwitterSpider(scrapy.Spider):
    name = "twitter_spider"
    start_urls = [
        "https://twitter.com/search?q=Scrapy"
    ]

    custom_settings = {
        'ITEM_PIPELINES': {
            'wow_classes.pipelines.TwPipeline': 500,
        }
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        # Extract the tweets from the page
        tweets = response.css('.tweet-text::text').getall()
        
        # Print the tweets
        for tweet in tweets:
            print(tweet)
        
        # Find the URL of the next page of search results
        next_page = response.css('.next-page::attr(href)').get()
        
        # Check if there is a next page
        if next_page:
            # Send a request to the next page
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse_page)

    def parse_page(self, response):
        # Extract the tweets from the page
        tweets = response.css('.tweet-text::text').getall()
        
        # Print the tweets
        for tweet in tweets:
            print(tweet)
        
        # Find the URL of the next page of search results
        next_page = response.css('.next-page::attr(href)').get()
        
        # Check if there is a next page
        if next_page:
            # Send a request to the next page
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse_page)