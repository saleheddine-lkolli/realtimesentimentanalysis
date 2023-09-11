import scrapy
from selenium.webdriver.common.by import By
from urllib.parse import urlencode 
from seleniumwire import webdriver
from twitterAPI.items import TweetItem
from scrapy.http.cookies import CookieJar
import json
from pathlib import Path
import time
from twitterAPI.settings import USER_AGENTS , ROTATING_PROXY_LIST,custom_job_settings
from twitterAPI.settings import SEARCH_KEYWORDS,NUM_OF_TWEETS ,PARSE_TWEETS_CONTENT_ONLY
from selenium.webdriver.chrome.options import Options
import random 
import os 



####################################
# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument('--headless')
# Choose a random User-Agent from the list
random_user_agent = random.choice(USER_AGENTS)
chrome_options.add_argument(f"--user-agent={random_user_agent}")

# randomly extract a proxy
random_proxy = random.choice(ROTATING_PROXY_LIST)
# set the proxy 
chrome_options.add_argument(f'--proxy-server={random_proxy}')


class TwitterSpider(scrapy.Spider):

    name = "twitter_spider"
    allowed_domains = ["twitter.com"]
    start_urls = ["https://twitter.com"]

    custom_settings = custom_job_settings()

    def save_cookies(self,webdriver):
        cookies_path = os.getcwd()+'/cookies.json'
        with Path(cookies_path).open('w') as f:
            f.write(json.dumps(webdriver.get_cookies(), indent=2))

    def get_cookies(self,webdriver):
        webdriver.delete_all_cookies()
        for cookie in json.loads(Path(os.getcwd()+'/cookies.json').read_text()):
            if not cookie['domain'].startswith('.'):
                cookie['domain'] = '.{}'.format(cookie['domain'])
            webdriver.add_cookie(cookie)

    def __init__(self, *args, **kwargs):
        super(TwitterSpider, self).__init__(*args, **kwargs)
        
        


    def start_requests(self):
        signin_url = 'https://twitter.com/home'
        yield scrapy.Request(
            url= signin_url,
            callback=self.check_login, 
            dont_filter=True,
        )
    def check_login(self, response):
        mdriver = webdriver.Chrome(options=chrome_options)
        mdriver.get(response.url)
        time.sleep(1)
        try:
            self.get_cookies(mdriver)
        except:
            self.log('Login needed')
        mdriver.get(response.url)
        time.sleep(3)
        if "HOME / X" in mdriver.title:
            self.log("No login needed for URL: " + response.url)
            mdriver.quit()
            yield scrapy.Request(url=response.url, callback=self.search_realTime)
        else:
            self.log("Login needed for URL: " + response.url)
            mdriver.quit()
            yield scrapy.Request(url=response.url, callback=self.login)

    def login(self, response):
        mdriver = webdriver.Chrome(options=chrome_options)
        mdriver.get('https://twitter.com/i/flow/login')
        time.sleep(3)
        email_input = mdriver.find_element('name','text')
        email_input.send_keys(self.custom_settings.get('USERNAME', 'BobyKlps65413'))
        next_button = mdriver.find_element('css selector', 'div.css-18t94o4.css-1dbjc4n.r-sdzlij.r-1phboty.r-rs99b7.r-ywje51.r-usiww2.r-2yi16.r-1qi8awa.r-1ny4l3l.r-ymttw5.r-o7ynqc.r-6416eg.r-lrvibr.r-13qz1uu')
        next_button.click()
        time.sleep(2)
        password_input = mdriver.find_element('name','password')        
        password_input.send_keys(self.custom_settings.get('PASSWORD', 'default_password'))
        login_button = mdriver.find_element('css selector','div.css-1dbjc4n.r-pw2am6')
        login_button.click()
        time.sleep(3)  # Allow time for the login to complete   
        self.save_cookies(mdriver)  
        url = mdriver.current_url
        mdriver.quit()          
        yield scrapy.Request(url=url, dont_filter=True, callback=self.search_realTime)
    
    def search_realTime(self,response):
        url=f"https://twitter.com/search?q={SEARCH_KEYWORDS.strip().replace(' ','%20')}%20lang%3Aen&src=typed_query&f=live"
        
        if PARSE_TWEETS_CONTENT_ONLY ==True :
            yield scrapy.Request(url=url, dont_filter=True, callback=self.parse_tweets_content_only)
        else:
            yield scrapy.Request(url=url, dont_filter=True, callback=self.parse_tweets)

    def search_Tope(self,response):
        url=f"https://twitter.com/search?q={SEARCH_KEYWORDS.strip().replace(' ','%20')}%20lang%3Aen&src=typed_query&f=top"
        yield scrapy.Request(url=url, dont_filter=True, callback=self.parse_tweets)
        
    def parse_tweets(self, response, **kwargs):
        mdriver = webdriver.Chrome(options=chrome_options)
        mdriver.get(response.url)
        time.sleep(1)
        self.get_cookies(mdriver)
        mdriver.get(response.url)
        tweets = []
        try:
            while len(tweets) < NUM_OF_TWEETS:
                time.sleep(0.5)
                tweets = mdriver.find_elements(By.XPATH,'//article[@data-testid="tweet"]')

            for i in range(0,NUM_OF_TWEETS):
                try:
                    url_item = tweets[i].find_element(By.CSS_SELECTOR, 'div.css-1dbjc4n.r-18u37iz.r-1q142lx a')
                    tweet_url = url_item.get_attribute('href')
                    tweet_item = self.parse_tweet(response=None,url=tweet_url)
                    yield tweet_item
                except:
                    pass
        except:
            print("***********************************************")
        mdriver.quit()

    def parse_tweet(self,response,url):
        print('***************************************parse_tweet start*********************************************')
        mdriver = webdriver.Chrome(options=chrome_options)
        mdriver.get(url)
        self.get_cookies(mdriver)
        mdriver.get(url)
        time.sleep(2)
        tweet_item = TweetItem()
        #######################################
        try:
            tweet_item['url'] = url
        except:
            tweet_item['url'] = ''
        #######################################
        try:
            tweet_item['author']  = mdriver.find_element(By.CSS_SELECTOR,"span span.css-901oao.css-16my406.r-poiln3.r-bcqeeo.r-qvutc0").text
        except:
            tweet_item['author'] = ''

        #######################################
        try:
            tweet_item['timestamp'] = mdriver.find_element(By.XPATH,".//time").get_attribute('datetime')
        except:
            tweet_item['timestamp'] = ''
        #######################################
        try:
            tweet_item['content'] = mdriver.find_element(By.XPATH,".//div[@data-testid='tweetText']").text
        except:
            tweet_item['content'] = ''
        #######################################
        try:
            tweet_item['likes'] = mdriver.find_element(By.CSS_SELECTOR,".css-1dbjc4n.r-1mf7evn.r-1yzf0co a[href*='/likes']").find_element(By.CSS_SELECTOR,"span.css-901oao.css-16my406").text
        except:
            tweet_item['likes'] = '00'
        #######################################
        try:
            tweet_item['views'] = mdriver.find_element(By.CSS_SELECTOR, 'div.css-1dbjc4n.r-xoduu5.r-1udh08x span span span').text
        except:
            tweet_item['views'] = '00'
        #######################################
        try:
            tweet_item['reposts'] = mdriver.find_element(By.CSS_SELECTOR,".css-1dbjc4n.r-1mf7evn.r-1yzf0co a[href*='/retweets']").find_element(By.CSS_SELECTOR,"span.css-901oao.css-16my406").text
        except:
            tweet_item['reposts'] = '00'
        #######################################
        """try:
            tweet_item['location'] = ''
        except:
            tweet_item['location'] = ''"""
        #######################################
        try:
            tweet_item['hashtags'] = ''
        except:
            tweet_item['hashtags'] = ''
        #######################################
        try:
            mentions = mdriver.find_element(By.XPATH,".//div[@data-testid='tweetText']").find_elements(By.TAG_NAME, "a")
            tweet_item['mentions'] = [a.text for a in mentions if a.text.startswith('@')]
        except:
            tweet_item['mentions'] = ''
        #######################################
        try:
            tweet_item['language'] = 'en'
        except:
            tweet_item['language'] = ''  
        #######################################
        try:
            replays = mdriver.find_elements(By.XPATH, '//article[@data-testid="tweet"]')
            tweet_item['replays'] = []
            if len(replays) > 1:
                for replay in replays:
                    replay_instance = TweetItem() 
                    try:
                        url_item = replay.find_element(By.CSS_SELECTOR,'div.css-1dbjc4n.r-18u37iz.r-1q142lx a')
                        tweet_url = url_item.get_attribute('href')
                        replay_instance = self.parse_tweet(response=None,url1=tweet_url)
                        tweet_item['replays'].append(replay_instance)
                    except:
                        pass
        except:
            tweet_item['replays'] = []

        mdriver.quit()
        return tweet_item
        #######################################
        


    def parse_tweets_content_only(self, response, **kwargs):
        mdriver = webdriver.Chrome(options=chrome_options)
        mdriver.get(response.url)
        time.sleep(1)
        self.get_cookies(mdriver)
        mdriver.get(response.url)
        tweets = []
        try:
            while len(tweets) < NUM_OF_TWEETS:
                time.sleep(0.5)
                tweets = mdriver.find_elements(By.XPATH,'//article[@data-testid="tweet"]')

            for i in range(0,NUM_OF_TWEETS):
                tweet_item = TweetItem()
                try:
                    url_item = tweets[i].find_element(By.CSS_SELECTOR, 'div.css-1dbjc4n.r-18u37iz.r-1q142lx a')
                    tweet_item['url'] = url_item.get_attribute('href')
                except:
                    tweet_item['url'] = ''
                #######################################
                try:
                    tweet_item['author']  = tweets[i].find_element(By.CSS_SELECTOR,"span span.css-901oao.css-16my406.r-poiln3.r-bcqeeo.r-qvutc0").text
                except: 
                    tweet_item['author'] = ''

                #######################################
                try:
                    tweet_item['timestamp'] = tweets[i].find_element(By.XPATH,".//time").get_attribute('datetime')
                except:
                    tweet_item['timestamp'] = ''
                #######################################
                try:
                    tweet_item['content'] = tweets[i].find_element(By.XPATH,".//div[@data-testid='tweetText']").text
                except:
                    tweet_item['content'] = ''
                #######################################
                yield tweet_item
        except:
            pass
        mdriver.quit()
        


    