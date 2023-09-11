# Scrapy settings for twitterAPI project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "twitterAPI"

SPIDER_MODULES = ["twitterAPI.spiders"]
NEWSPIDER_MODULE = "twitterAPI.spiders"

"""FEEDS = {
     'tweetsdata.json' : {'format': 'json'} 
 }"""

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "twitterAPI (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
    #"twitterAPI.middlewares.TwitterapiSpiderMiddleware": 543,
    
}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {

    #"twitterAPI.middlewares.TwitterapiDownloaderMiddleware": 543,
    
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    "twitterAPI.pipelines.TwitterapiPipeline": 300,
    'twitterAPI.pipelines.KafkaPipeline': 400,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
###

# Keywords to search for in tweets
SEARCH_KEYWORDS = 'bad experience'

# Number of tweets to retrieve
NUM_OF_TWEETS = 3

# Flag to determine whether to parse only the content of tweets True or False
PARSE_TWEETS_CONTENT_ONLY = True

# Twitter account credentials
# settings.py

# Define custom command-line arguments
from scrapy.utils.project import get_project_settings
settings = get_project_settings()

custom_settings = {
    'job01': {
        'USERNAME': 'BobyKlps65413',
        'PASSWORD': 'kUm9:%bg2iPq8i,',
    },
    'job02': {
        'USERNAME': 'BobyKlps65413',
        'PASSWORD': 'kUm9:%bg2iPq8i,',
    },
    'job03': {
        'USERNAME': 'BobyKlps65413',
        'PASSWORD': 'kUm9:%bg2iPq8i,',
    },
    # Define settings for other jobs here
}

def custom_job_settings():
    job_id = getattr(settings, 'job_id', 'job01')
    return custom_settings.get(job_id, {})

# Use Scrapy's command-line arguments to override settings
USERNAME = getattr(settings, 'USERNAME', 'BobyKlps65413')
PASSWORD = getattr(settings, 'PASSWORD', 'kUm9:%bg2iPq8i,')


# List of rotating proxy servers
ROTATING_PROXY_LIST = [
'64.56.150.102:3128',
'172.105.107.223:3128',
'51.222.155.142:80',
'190.113.40.202:999',
'201.229.250.21:8080',
'45.229.34.174:999',
'190.89.37.73:999',
'185.123.143.251:3128',
'185.123.143.247:3128',
'37.120.140.158:3128',
'191.97.16.160:999',
'201.249.152.172:999',
'191.97.19.66:999',
'102.38.17.193:8080',
'41.254.53.70:1981',
'102.38.22.121:8080',
'85.221.249.213:8080',
'194.31.53.250:80',
'153.19.91.77:80',
'43.255.113.232:84',
'203.189.150.48:8080',
'103.216.51.36:32650',
'200.24.130.138:999',
'157.100.6.202:999',
'181.39.27.225:1994',
'45.235.123.45:999',
'190.128.241.102:80',
'181.120.28.228:80',
'118.99.108.4:8080',
'104.25.87.42:80',
'103.38.205.17:5678',
'106.75.173.225:999',
'168.205.217.58:4145',
'177.38.5.254:4153',
'173.177.85.227:80',
'132.148.153.131:14731',
'45.188.166.52:1994',
'45.231.221.193:999',
'189.250.135.40:80',
'177.229.210.50:8080',
'159.89.113.155:8080',
]

# List of User-Agent strings
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'

]

# List of Kafka broker addresses
KAFKA_PRODUCER_BROKERS = ["192.168.1.101:9092"]

# Kafka producer configuration settings
KAFKA_PRODUCER_CONFIGS = {"client_id": "id01", "retries": 1}

# Kafka producer topic to which messages will be sent
KAFKA_PRODUCER_TOPIC = "twitter01"

# Log level for Kafka producer (e.g., DEBUG, INFO, etc.)
KAFKA_PRODUCER_LOGLEVEL = "DEBUG"

# Timeout (in mili=seconds) for gracefully closing the Kafka producer
KAFKA_PRODUCER_CLOSE_TIMEOUT = 5000 

# Flag to ensure that Kafka message values are encoded in base64
KAFKA_VALUE_ENSURE_BASE64 = True

# List of fields to be filtered when exporting data to Kafka
KAFKA_EXPORT_FILTER = ["filtered_field"]