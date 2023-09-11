import scrapy
from twitterAPI.settings import PARSE_TWEETS_CONTENT_ONLY

class TwitterapiItem(scrapy.Item):
    # Define the fields for your item here like:
    # name = scrapy.Field()
    pass


class TweetItem(scrapy.Item):
    # Define the fields for your Tweet item here:
    url = scrapy.Field()
    author = scrapy.Field()
    timestamp = scrapy.Field()
    content = scrapy.Field()
    if PARSE_TWEETS_CONTENT_ONLY == True :
        views = scrapy.Field()
        likes = scrapy.Field()
        reposts = scrapy.Field()
        replays = scrapy.Field()  
        hashtags = scrapy.Field() 
        mentions = scrapy.Field() 
        language = scrapy.Field()
 
    