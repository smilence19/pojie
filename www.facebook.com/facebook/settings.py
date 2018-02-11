# -*- coding: utf-8 -*-

# Scrapy settings for facebook project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'facebook'

SPIDER_MODULES = ['facebook.spiders']
NEWSPIDER_MODULE = 'facebook.spiders'


SPLASH_URL = 'http://127.0.0.1:8050'

DEFAULT_REQUEST_HEADERS = {
  'Accept': 'application/json,text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  # 'Referer': 'http://tv.sohu.com/drama/',
  # 'Host': 'so.tv.sohu.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/11.0.2 Safari/604.4.7',
    # 'access_token': 'EAARDVcuRmWMBAIrdA6OoVDZCqh4LZBpfZAIrdoZCe1D9EMcmRWgi4AVz24ruWIr8laNTw9rP6kFHlaBPWBGTjo4BWUZC2nIF7AKFr2t4ZB17qSvb4UbTt4E8QfkprCafPuP2g7CA5UHkdswBNZACQ2t1wQ1JZCBjqfAZD',
    'Connection': 'keep-alive',
  # 'Cookie': 'Hm_lvt_082a80ccf2db99dbd7b5006fe0744b57=1476433353,1476859804,1477905972; ch_key=50e48c6168d7b908; fuid=14593949145193150340; landingrefer=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DVwhH67b0ynpcV5GddrjzWj1EK6Z1lW_tURWK8cvIaEG%26wd%3D%26eqid%3D8be210a00004014600000003581c4b33; IPLOC=CN1100; SUV=1603290957248103; _ga=GA1.2.443870539.1466419933; _smuid=UapWsu9Ece1ARdjXVyLboQ; beans_dmp=%7B%22admaster%22%3A1477905971%2C%22shunfei%22%3A1477905971%2C%22reachmax%22%3A1477655298%2C%22lingji%22%3A1477905971%2C%22yoyi%22%3A1477905971%2C%22ipinyou%22%3A1477905971%2C%22ipinyou_admaster%22%3A1477905971%2C%22jingzan%22%3A1477905971%2C%22miaozhen%22%3A1477905971%2C%22aodian%22%3A1477905971%2C%22diantong%22%3A1477655298%2C%22mediav1%22%3A1477996614%7D; gn12=w:1; sci12=w:1; shenhui12=w:1; skey=%7B%22key%22%3A%22%E7%94%98%E5%91%B3%E4%BA%BA%E7%94%9F%22%7D%2C%7B%22key%22%3A%22%E5%B7%BE%E5%B8%BC%E6%9E%AD%E9%9B%84%E4%B9%8B%E5%96%8B%E8%A1%80%E9%95%BF%E5%A4%A9%E5%9B%BD%E8%AF%AD%E7%B2%A4%E8%AF%AD%22%7D; sohutag=8HsmeSc5MCwmcyc5NSwmYjc5NTAsJ2EmOiUsJ2YmOiAsJ2cmOiAsJ24mOiYsJ2kmOiEsJ3cmOiQsJ2gmOiAsJ2NmOiEsJ2UmOiQsJ20mOiEsJ3QmOiB9; vjlast=1469349117.1478249294.11; vjuids=-7c84ddf08.153cab5d707.0.da229d9e',
  # 'Accept-Encoding': 'gzip, deflate',
}

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.8 (KHTML, like Gecko) Version/9.1.3 Safari/601.7.8'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'facebook (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
FILES_STORE = '/Users/huangqingjun/git/www.facebook.com'
FILES_URLS_FIELD = "file_urls"
# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16
DOWNLOADER_MIDDLEWARES = {
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}
SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}
# HTTP_PROXY = 'http://192.168.1.103:3213'
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'
# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'facebook.middlewares.FacebookSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'facebook.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'facebook.pipelines.FacebookPipeline': 300,
   # 'facebook.pipelines.MyFilesPipeline': 1,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
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
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
