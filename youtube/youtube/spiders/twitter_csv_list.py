# -*- coding: utf-8 -*-
import scrapy
import time
import json
import csv
from youtube.items import TwitterItem
import os

class WeiboListSpider(scrapy.Spider):
    name = 'twitter_cvs_list'
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
    last_dateTime = int(time.time()*1000)
    # def start_requests(self):
    #     for url in self.start_urls:
    #         yield scrapy.Request(url=url, callback=self.parse,method='GET',cookies=self.cookie,headers=self.header)

    def start_requests(self):
        now_time = self.last_dateTime
        yes_time = now_time + (-7 * 24 *60 *60*1000)
        self.last_dateTime = yes_time
        yield scrapy.Request(
                url='https://analytics.twitter.com/user/cgtnfrancais/tweets/export.json?start_time='+str(yes_time)+'&end_time='+str(now_time)+'&lang=zh-cn',
                callback=self.list_parse, method='POST', cookies=self.cookie)

    def list_parse(self, response):
        print(response.text)

        ajson = json.loads(response.text)
        has_next_page = ajson['status']
        if has_next_page == 'Available':
            yield scrapy.Request(
                url=response.url.replace("export.json","bundle"),
                callback=self.cvs_parse, method='GET', cookies=self.cookie)
        else:
            time.sleep(5)
            yield scrapy.Request(
                url=response.url,
                callback=self.list_parse, method='POST', cookies=self.cookie,dont_filter=True)

    def cvs_parse(self, response):
        fh = open("csv/"+str(self.last_dateTime)+'.csv', 'w')
        fh.write(response.text)
        fh.close()
        # csv_file = csv.reader(open('dairly_csv.csv', 'r'))
        # n = 0
        # for i in csv_file:
        #     n = n + 1
        #     if n <= 2:
        #         continue
        #     print(i)

        now_time = self.last_dateTime
        yes_time = now_time + (-7 * 24 *60 *60*1000)
        self.last_dateTime = yes_time
        time.sleep(60)
        if now_time > 1393891200000:
            yield scrapy.Request(
                url='https://analytics.twitter.com/user/cgtnfrancais/tweets/export.json?start_time=' + str(
                    yes_time) + '&end_time=' + str(now_time) + '&lang=zh-cn',
                callback=self.list_parse, method='POST', cookies=self.cookie)
    #批量入库
        else:
            filename_list = []
            for root, dirs, files in os.walk('/Users/huangqingjun/git/youtube/csv'):
                print(files)
                filename_list = files
            for file_name in filename_list:
                print(file_name)
                if '.DS_Store' in file_name:
                    continue
                csv_file = csv.reader(open('/Users/huangqingjun/git/youtube/csv/' + file_name, 'r'))
                n = 0
                for i in csv_file:
                    if n == 0:
                        n = 1
                        continue

                    item = TwitterItem()
                    item['post_id'] = i[0]
                    item['post_message'] = i[2]
                    item['post_url'] = i[1]
                    item['post_create_time'] = i[3]
                    item['post_show_times'] = i[4]
                    item['post_hudong_times'] = i[5]
                    item['post_hudong_rate'] = i[6]
                    item['post_shares_times'] = i[7]
                    item['post_comments_times'] = i[8]
                    item['post_like_times'] = i[9]
                    item['post_url_click_count'] = i[11]
                    item['post_video_watch_times'] = i[20]
                    item['post_video_hudong_times'] = i[21]
                    if i[22] == '-':
                        item['post_show_times_fee'] = 0
                    else:
                        item['post_show_times_fee'] = i[22]
                    if i[23] == '-':
                        item['post_hudong_times_fee'] = 0
                    else:
                        item['post_hudong_times_fee'] = i[23]

                    item['post_hudong_rate_fee'] = i[24]

                    if i[25] == '-':
                        item['post_shares_times_fee'] = 0
                    else:
                        item['post_shares_times_fee'] = i[25]

                    if i[26] == '-':
                        item['post_comments_times_fee'] = 0
                    else:
                        item['post_comments_times_fee'] = i[26]

                    if i[27] == '-':
                        item['post_like_times_fee'] = 0
                    else:
                        item['post_like_times_fee'] = i[27]

                    if i[29] == '-':
                        item['post_url_click_count_fee'] = 0
                    else:
                        item['post_url_click_count_fee'] = i[29]

                    if i[38] == '-':
                        item['post_video_watch_times_fee'] = 0
                    else:
                        item['post_video_watch_times_fee'] = i[38]

                    if i[39] == '-':
                        item['post_video_hudong_times_fee'] = 0
                    else:
                        item['post_video_hudong_times_fee'] = i[39]
                    yield item









