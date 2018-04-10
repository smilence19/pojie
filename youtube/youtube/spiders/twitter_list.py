# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
import base64
import time
import json
from lxml import etree
import re
from youtube.items import WeiboItem
from scrapy.http import HtmlResponse

class WeiboListSpider(scrapy.Spider):
    name = 'twitter_list'
    allowed_domains = ['analytics.twitter.com']
    start_urls = [
        'https://analytics.twitter.com/user/cgtnfrancais/tweets/timeline.json?start_time=1512691200000&max_id=0&end_time=1520553599999&page_end_time=1520553599999&page=0&filter=no_replies&metric=clicks&lang=zh-cn'
        ]

    lua_script = """
      function main(splash)
        splash:on_request(
            function(request)
                request:set_header('Cookie','twttr_ads_sess=BAh7CDoPY3JlYXRlZF9hdGwrCCxrkABiASIQX2NzcmZfdG9rZW4iJTQyZDIx%0AMjg1NTU0N2QzYmU2YzEwN2YzMDI5ODc1MDFhIg9zZXNzaW9uX2lkIiU0OWU5%0ANjZiYTU5YTViNzZmNmFlMTdmMGE5OWI2NzM3Nw%3D%3D--6e703ab542c3cf400332141495c456385986d7eb; lang=zh-cn; _twitter_sess=BAh7CiIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCD%252FRgABiAToMY3NyZl9p%250AZCIlYTgwMmRjZGEwYjJjMWE4NmQ2YjU1NDA1ZTIxYjQ5NmU6B2lkIiUwYTVj%250AYzYzNDZhMzY3ZGM0ODUxOWFlMWQyMDgzMWUyNjoJdXNlcmwrB2rhXmM%253D--2768e3333a7b0f23eda5b064f0a26d1212ba0952; ct0=498db128165277752e4101788786b3ac; _uetsid=_uetcae11eb9; _ga=GA1.2.927823815.1511333324; _gid=GA1.2.495692354.1520426947; ads_prefs="HBIRAAA="; auth_token=0e57b47ad4cccd4f0aa8293053a1b69a03a26e52; kdt=I5YqdyrrJkdRBeOT4QSWkoCglQS6YZjKXai3S16r; remember_checked_on=1; twid="u=1667162474"; guest_id=v1%3A152042694270054249; personalization_id="v1_7WjDy1tap3vrPGqSeLbQ1Q=="')
    		end)
  	    splash:go(splash.args.url)
  	    splash:wait(12)
  			local scroll_to = splash:jsfunc("window.scrollTo")
  			scroll_to(0, 300)
        return {
        html = splash:html(),
        png = splash:png(),
        har = splash:har(),
  }
end
    """

    cookie = {
        'twttr_ads_sess': 'BAh7CDoPY3JlYXRlZF9hdGwrCCxrkABiASIQX2NzcmZfdG9rZW4iJTQyZDIx%0AMjg1NTU0N2QzYmU2YzEwN2YzMDI5ODc1MDFhIg9zZXNzaW9uX2lkIiU0OWU5%0ANjZiYTU5YTViNzZmNmFlMTdmMGE5OWI2NzM3Nw%3D%3D--6e703ab542c3cf400332141495c456385986d7eb',
        'lang': 'zh-cn',
        '_twitter_sess': 'BAh7CiIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCD%252FRgABiAToMY3NyZl9p%250AZCIlYTgwMmRjZGEwYjJjMWE4NmQ2YjU1NDA1ZTIxYjQ5NmU6B2lkIiUwYTVj%250AYzYzNDZhMzY3ZGM0ODUxOWFlMWQyMDgzMWUyNjoJdXNlcmwrB2rhXmM%253D--2768e3333a7b0f23eda5b064f0a26d1212ba0952',
        'ct0': '498db128165277752e4101788786b3ac', '_uetsid': '_uetcae11eb9', '_ga': 'GA1.2.927823815.1511333324',
        '_gid': 'GA1.2.495692354.1520426947', 'ads_prefs': '"HBIRAAA="',
        'auth_token': '0e57b47ad4cccd4f0aa8293053a1b69a03a26e52', 'kdt': 'I5YqdyrrJkdRBeOT4QSWkoCglQS6YZjKXai3S16r',
        'remember_checked_on': '1', 'twid': '"u=1667162474"', 'guest_id': 'v1%3A152042694270054249',
        'personalization_id': '"v1_7WjDy1tap3vrPGqSeLbQ1Q=="'
        }
    header = {
        'Referer': 'https://analytics.twitter.com/user/cgtnfrancais/tweets',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'www.youtube.com',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Connection': 'keep-alive',
        'Accept-Language': 'zh-cn',
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0.3 Safari/604.5.6',
        'X-Requested-With':'XMLHttpRequest'
    }

    # def start_requests(self):
    #     for url in self.start_urls:
    #         yield scrapy.Request(url=url, callback=self.parse,method='GET',cookies=self.cookie,headers=self.header)

    def start_requests(self):

        yield scrapy.Request(
                url='https://analytics.twitter.com/user/cgtnfrancais/tweets/timeline.json?start_time=1512691200000&max_id=0&end_time=1520553599999&page_end_time=1520553599999&page=0&filter=no_replies&metric=clicks&lang=zh-cn',
                callback=self.list_parse, method='GET', cookies=self.cookie)

    def list_parse(self, response):
        # print(response.text)

        ajson = json.loads(response.text)
        data = ajson['data']
        has_next_page = ajson['hasNext']

        aresponse = HtmlResponse(url=response.url, body=data, encoding='utf-8')

        list = aresponse.xpath("//li[@class = 'topn-page tweet-activity-tweet-group']")
        for item in list:
            post_id = item.xpath("./@data-tweet-id").extract()[0]
            post_create_time = item.xpath("./ul/div/li/div[1]/div/div/div/span[1]/a/text()").extract()[0]

            post_msg = item.xpath("./ul/div/li/div[1]/div/div/div/span[2]/text()").extract()[0]
            a_list = item.xpath(".//ul/div/li/div[1]/div/div/div/span[2]/a")
            for aitem in a_list:
                link = aitem.xpath("./b/text()").extract()
                if len(link):
                    link_text = "#"+link[0]

            post_show_times = item.xpath(".//div[@class = 'tweet-activity-data impressions text-right col-md-1']/text()").extract()[0]
            post_hudong_times = item.xpath(".//li/div[3]/text()").extract()[0]
            post_hudong_rate = item.xpath(".//li/div[4]/text()").extract()[0]
            print(list.index(item))
            if list.index(item) == len(list)-1:
                yield scrapy.Request(
                    url='https://analytics.twitter.com/user/cgtnfrancais/tweets/timeline.json?start_time=1512691200000&max_id='+post_id+'&end_time=1520553599999&page_end_time=1520553599999&page=0&filter=no_replies&metric=clicks&lang=zh-cn',
                    callback=self.list_parse, method='GET', cookies=self.cookie)







