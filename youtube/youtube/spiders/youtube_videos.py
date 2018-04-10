# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
import base64
from youtube.items import YoutubeItem,YoutubeContentItem
import re
import datetime

class YoutubeVideosSpider(scrapy.Spider):
    name = 'youtube_videos'
    allowed_domains = ['www.youtube.com']
    start_urls = [
        'https://www.youtube.com/my_videos?o=U&pi=101',
        #           'http://127.0.0.1:8050/info?wait=0.5&images=1&expand=1&timeout=90.0&url=https%3A%2F%2Fwww.youtube.com%2Fmy_videos%3Fo%3DU&lua_source=function+main%28splash%29%0D%0A++++splash.images_enabled+%3D+false%0D%0A++++splash%3Aon_request%28%0D%0A++++++++++++function%28request%29%0D%0A++++++++++++++++request%3Aset_header%28%27Cookie%27%2C%27PREF%3Df1%3D50000000%26f4%3D4000000%26f5%3D30%26al%3Dzh-CN%3B+_ga%3DGA1.2.1551080313.1519631749%3B+_gid%3DGA1.2.2107864435.1519631749%3B+LOGIN_INFO%3DAFmmF2swRAIga-UgsgOu93L7QY924vDoA9nf8S_TohHgl2_xIWMlsiwCIDZ3_yNPtZ-EU1mjQ22fiyBQr-eiOi_v-5psiqvl0Hl7%3AQUQ3MjNmelN3cDFHQkVUYnliVEl6bUEwbXh1eXh6SUhFOEI0UzdneXFlTlNDMVNYSnp5a3FCVEFvcV9kSEF6d0Q5aG50VnFnMno2UExqX3lTV3Z1NlYxZDlYR1dBTVVqbHFEdWdnbEJCV0JOZTdtSG9YVlo1eDVpYWNPd2Uyd1p1bmtsWV90R29xamlvakZIWWFOZFBrQTRmQlNlanJIcWZjaHFMOXBmQk5qVElVTXJvNGZNUmtDQllYc3d1cDJ1OHdCVmNhV2F2MFRxT2NKV3JWVENYQTh4Z3lzRWc4RlZaMDhFWmJxYlN2MnFfTjE2bmY0WWNFSQ%3D%3D%3B+APISID%3DCkD4QszXZD8TZUhA%2FAeO9cled_EL-9Hug_%3B+HSID%3DAtAiFrHalcv0TSlO2%3B+SAPISID%3DMgS2b-gUXC9kUQLs%2FAbIclDQc8r_M3c5To%3B+SID%3D0QWNn1dj70Lx9UnnP7fuR2sLUJOflNeBAf5Mo_KQ1wMLrMwSvuAN8IBESCTLCTCEos7t3A.%3B+SSID%3DApD50x2AlXSHSaz5E%3B+YSC%3Dk5jRk2PEUfE%3B+VISITOR_INFO1_LIVE%3DWQWqeYMqwiA%27%29%0D%0A++++++++++++end%29%0D%0A++%09splash%3Ago%28splash.args.url%29%0D%0A++%09splash%3Await%285%29%0D%0A++++return+%7B%0D%0A++++html+%3D+splash%3Ahtml%28%29%2C%0D%0A++++png+%3D+splash%3Apng%28%29%2C%0D%0A++++har+%3D+splash%3Ahar%28%29%2C%0D%0A++%7D%0D%0Aend']
        ]

    lua_script = """
    function wait_for_element(splash, css, maxwait)
  -- Wait until a selector matches an element
  -- in the page. Return an error if waited more
  -- than maxwait seconds.
  if maxwait == nil then
      maxwait = 20
  end
  return splash:wait_for_resume(string.format([[
    function main(splash) {
      var selector = '%s';
      var maxwait = %s;
      var end = Date.now() + maxwait*1000;

      function check() {
        if(document.querySelector(selector)) {
          splash.resume('Element found');
        } else if(Date.now() >= end) {
          var err = 'Timeout waiting for element';
          splash.error(err + " " + selector);
        } else {
          setTimeout(check, 200);
        }
      }
      check();
    }
  ]], css, maxwait))
end
    function main(splash)
        splash:on_request(
            function(request)
                request:set_header('Cookie','_ga=GA1.2.1551080313.1519631749; _gid=GA1.2.2107864435.1519631749; PREF=f1=50000000&f4=4000000&f5=30&al=zh-CN; LOGIN_INFO=AFmmF2swRAIga-UgsgOu93L7QY924vDoA9nf8S_TohHgl2_xIWMlsiwCIDZ3_yNPtZ-EU1mjQ22fiyBQr-eiOi_v-5psiqvl0Hl7:QUQ3MjNmelN3cDFHQkVUYnliVEl6bUEwbXh1eXh6SUhFOEI0UzdneXFlTlNDMVNYSnp5a3FCVEFvcV9kSEF6d0Q5aG50VnFnMno2UExqX3lTV3Z1NlYxZDlYR1dBTVVqbHFEdWdnbEJCV0JOZTdtSG9YVlo1eDVpYWNPd2Uyd1p1bmtsWV90R29xamlvakZIWWFOZFBrQTRmQlNlanJIcWZjaHFMOXBmQk5qVElVTXJvNGZNUmtDQllYc3d1cDJ1OHdCVmNhV2F2MFRxT2NKV3JWVENYQTh4Z3lzRWc4RlZaMDhFWmJxYlN2MnFfTjE2bmY0WWNFSQ==; APISID=CkD4QszXZD8TZUhA/AeO9cled_EL-9Hug_; HSID=AtAiFrHalcv0TSlO2; SAPISID=MgS2b-gUXC9kUQLs/AbIclDQc8r_M3c5To; SID=0QWNn1dj70Lx9UnnP7fuR2sLUJOflNeBAf5Mo_KQ1wMLrMwSvuAN8IBESCTLCTCEos7t3A.; SSID=ApD50x2AlXSHSaz5E; YSC=k5jRk2PEUfE; VISITOR_INFO1_LIVE=WQWqeYMqwiA')
            end)
  	    splash:go(splash.args.url)
  	    wait_for_element(splash, "span.vm-date-info")
        return {
        html = splash:html(),
        png = splash:png(),
        har = splash:har(),
  }
end
    """

    cookie = {'Cookie':'PREF=f1=50000000&f4=4000000&f5=30&al=zh-CN; _ga=GA1.2.1551080313.1519631749; _gid=GA1.2.2107864435.1519631749; LOGIN_INFO=AFmmF2swRAIga-UgsgOu93L7QY924vDoA9nf8S_TohHgl2_xIWMlsiwCIDZ3_yNPtZ-EU1mjQ22fiyBQr-eiOi_v-5psiqvl0Hl7:QUQ3MjNmelN3cDFHQkVUYnliVEl6bUEwbXh1eXh6SUhFOEI0UzdneXFlTlNDMVNYSnp5a3FCVEFvcV9kSEF6d0Q5aG50VnFnMno2UExqX3lTV3Z1NlYxZDlYR1dBTVVqbHFEdWdnbEJCV0JOZTdtSG9YVlo1eDVpYWNPd2Uyd1p1bmtsWV90R29xamlvakZIWWFOZFBrQTRmQlNlanJIcWZjaHFMOXBmQk5qVElVTXJvNGZNUmtDQllYc3d1cDJ1OHdCVmNhV2F2MFRxT2NKV3JWVENYQTh4Z3lzRWc4RlZaMDhFWmJxYlN2MnFfTjE2bmY0WWNFSQ==; APISID=CkD4QszXZD8TZUhA/AeO9cled_EL-9Hug_; HSID=AtAiFrHalcv0TSlO2; SAPISID=MgS2b-gUXC9kUQLs/AbIclDQc8r_M3c5To; SID=0QWNn1dj70Lx9UnnP7fuR2sLUJOflNeBAf5Mo_KQ1wMLrMwSvuAN8IBESCTLCTCEos7t3A.; SSID=ApD50x2AlXSHSaz5E; YSC=k5jRk2PEUfE; VISITOR_INFO1_LIVE=WQWqeYMqwiA'}
    header = {
        'Referer': 'https://www.youtube.com/my_videos?o=U',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'www.youtube.com',
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'Accept-Language': 'zh-cn',
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0.3 Safari/604.5.6'
    }

    last_dateTime = datetime.datetime.now()


    # def start_requests(self):
    #     for url in self.start_urls:
    #         yield scrapy.Request(url=url, callback=self.parse,method='GET',cookies=self.cookie,headers=self.header)

    def start_requests(self):

        now_time = self.last_dateTime
        yes_time = now_time + datetime.timedelta(days=-30)
        self.last_dateTime = yes_time
        now_data = now_time.strftime('%Y-%m-%d')
        yes_date = yes_time.strftime('%Y-%m-%d')

        for url in self.start_urls:
            yield SplashRequest(
                # url='https://www.youtube.com/my_videos?o=U&sq=after%3A2018-01-12+before%3A2018-02-11&pi=3',
                url='https://www.youtube.com/my_videos?o=U&sq=after%3A'+yes_date+'+before%3A'+now_data+'&pi=1', callback=self.parse,
                                args={'wait': 0.5,
                                      'png':1,
                                      'html':1,
                                      'lua_source': self.lua_script,
                                      }, endpoint='execute')
    def parse(self, response):


        f = open('test.png', 'wb')  # 若是'wb'就表示写二进制文件
        f.write(base64.b64decode(response.data['png']))
        f.close()

        ol_list = response.xpath("//ol[@class = 'vm-video-list']/li")
        for item in ol_list:

            init_item = YoutubeItem()
            post_id_list = item.xpath("./div/@data-video-id").extract()
            if len(post_id_list):
                init_item['post_id'] = post_id_list[0]
            tilte_list = item.xpath(".//div[@class = 'vm-video-info-container']/div[@class = 'vm-video-title']/div/a")
            if len(tilte_list):
                init_item['post_video_url'] = "https://www.youtube.com"+item.xpath(".//div[@class = 'vm-video-info-container']/div[@class = 'vm-video-title']/div/a/@href").extract()[0]
            else:
                continue
            post_video_title = item.xpath(
                ".//div[@class = 'vm-video-info-container']/div[@class = 'vm-video-title']/div/a/text()").extract()[0]
            hd_list = item.xpath(".//div[@class = 'vm-video-info-container']/div[@class = 'vm-video-title']/div/span")
            hd_msg = ''
            if len(hd_list):
                hd_msg = hd_list[0].xpath("./span/text()").extract()
                if len(hd_msg):
                    hd_msg = hd_msg[0]
                else:
                    hd_msg = ''
            init_item['post_video_title'] = post_video_title + ' '+ hd_msg

            time_list = item.xpath(".//div[@class = 'vm-video-info-container']/div[@class = 'vm-video-info']/span[@class = 'vm-date-info']")
            if len(time_list):
                print(time_list[0].extract())
                init_item['post_create_time'] = time_list[0].xpath("./span[1]/text()").extract()[0].replace("年","-").replace("月","-").replace("日","")
                time_hour_list = time_list[0].xpath("./span[2]/text()").extract()
                if len(time_hour_list):
                    init_item['post_create_time'] = init_item['post_create_time'] +" "+time_hour_list[0]
            else:
                init_item['post_video_title'] = '#直播#' + init_item['post_video_title']
                test_datetime = item.xpath(".//div[@class = 'vm-video-info-container']/div[@class = 'vm-video-info']/text()").extract()[0].replace("年","-").replace("月","-").replace("日","")
                mat = re.search(r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2})", test_datetime)
                if mat:
                    init_item['post_create_time'] = mat.group(0)
                else:
                    init_item['post_create_time'] = ''

            post_watch_times_list = item.xpath(".//div[@class = 'vm-video-side-view-count']/a/text()").extract()
            if len(post_watch_times_list):
                init_item['post_watch_times'] = post_watch_times_list[0].replace(" ", '').replace(
                "\n", '').replace("次观看", '').replace(",",'')
            else:
                init_item['post_watch_times'] = 0

            post_video_duration_list = item.xpath(
                ".//div[@class = 'vm-video-item-content']/div[@class = 'vm-video-item-content-primary']/div/span/span/text()").extract()
            if len(post_video_duration_list):
                init_item['post_video_duration'] = post_video_duration_list[0]
            else:
                init_item['post_video_duration'] = ''

            comment_list = item.xpath(
                ".//div[@class = 'vm-video-item-content']/div[@class = 'vm-video-item-content-secondary']/div/div/span/span/span/span[3]/text()").extract()
            if len(comment_list):
                init_item['post_comment_times'] = comment_list[0].replace(" ", '').replace("\n", '').replace(",",'')
            else:
                comment_list_new =  item.xpath(
                    ".//div[@class = 'vm-video-item-content']/div[@class = 'vm-video-item-content-secondary']/div/div/a/span/span/span[3]/text()").extract()
                if len(comment_list_new):
                    init_item['post_comment_times'] = comment_list_new[
                    0].replace(" ", '').replace("\n", '').replace(",",'')
                else:
                    init_item['post_comment_times'] = 0

            post_like_times_list = item.xpath(
                ".//div[@class = 'vm-video-item-content']/div[@class = 'vm-video-item-content-secondary']/div/div/a/span[1]/span/span[3]/text()").extract()
            if len(post_like_times_list):
                init_item['post_like_times'] = post_like_times_list[
                0].replace(" ", '').replace("\n", '').replace(",",'')
            else:
                init_item['post_like_times'] = 0
            post_dislike_timeslist = item.xpath(
                ".//div[@class = 'vm-video-item-content']/div[@class = 'vm-video-item-content-secondary']/div/div/a/span[2]/span/span[3]/text()").extract()
            if len(post_dislike_timeslist):
                init_item['post_dislike_times'] = post_dislike_timeslist[
                0].replace(" ", '').replace("\n", '').replace(",",'')
            else:
                init_item['post_dislike_times'] = 0


            if len(init_item['post_video_url']):
                yield scrapy.Request(
                    url=init_item['post_video_url'].replace('edit?o=U&video_id=','watch?v=')+'&feature=youtu.be',
                    # url='https://www.youtube.com/watch?v=z9gMT5EK4hs&feature=youtu.be',
                    callback=self.content_parse, method='GET', cookies=self.cookie)

            if len(init_item['post_id']):
                yield init_item

        if len(ol_list):

            range = response.url.index('&pi=')
            page = int(response.url[range+4:])+1
            aurl = response.url[:range+4]
            yield SplashRequest(url=aurl+str(page), callback=self.parse,
                                args={'wait': 0.5,
                                      'png': 1,
                                      'html': 1,
                                      'lua_source': self.lua_script,
                                      }, endpoint='execute',headers={
        'Referer': response.url,
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'www.youtube.com',
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'Accept-Language': 'zh-cn',
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0.3 Safari/604.5.6'
    })
        else:
            now_time = self.last_dateTime
            yes_time = now_time + datetime.timedelta(days=-30)
            self.last_dateTime = yes_time
            now_data = now_time.strftime('%Y-%m-%d')
            yes_date = yes_time.strftime('%Y-%m-%d')
            yield SplashRequest(
                url='https://www.youtube.com/my_videos?o=U&sq=after%3A' + yes_date + '+before%3A' + now_data + '&pi=1' , callback=self.parse,
                args={'wait': 0.5,
                      'png': 1,
                      'html': 1,
                      'lua_source': self.lua_script,
                      }, endpoint='execute', headers={
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Host': 'www.youtube.com',
                    'Accept': '*/*',
                    'Connection': 'keep-alive',
                    'Accept-Language': 'zh-cn',
                    'Accept-Encoding': 'gzip, deflate',
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0.3 Safari/604.5.6'
                })
        pass

    def content_parse(self, response):
        pp = re.compile(r'"shortDescription":"(.*?)",')
        matcher1 = re.search(pp, response.text)
        if matcher1:
            init_item = YoutubeContentItem()
            init_item['post_id'] = response.url.replace('&feature=youtu.be','').replace('https://www.youtube.com/watch?v=','')
            init_item['post_video_msg'] = matcher1.group(1).replace('\"','"').replace("\\n"," ").replace('YouTube :  https://www.youtube.com/c/CGTNFrancais Abonnez-vous sur : Facebook : https://www.facebook.com/CGTNFrancais/  Twitter : https://twitter.com/CGTNFrancais Instagram : https://www.instagram.com/cgtnfrancais/','')
            print(init_item['post_video_msg'])
            yield init_item
        else:
            yield SplashRequest(
                url=response.url,
                callback=self.splash_content_parse,
                args={'wait': 0.5,
                      'png': 1,
                      'html': 1,
                      'lua_source': self.lua_script,
                      }, endpoint='execute')


    def splash_content_parse(self, response):
        pp = re.compile(r'"shortDescription":"(.*?)",')
        matcher1 = re.search(pp, response.text)
        if matcher1:
            init_item = YoutubeContentItem()
            init_item['post_id'] = response.url.replace('&feature=youtu.be','').replace('https://www.youtube.com/watch?v=','')
            init_item['post_video_msg'] = matcher1.group(1).replace('\"','"').replace("\\n"," ").replace('YouTube :  https://www.youtube.com/c/CGTNFrancais Abonnez-vous sur : Facebook : https://www.facebook.com/CGTNFrancais/  Twitter : https://twitter.com/CGTNFrancais Instagram : https://www.instagram.com/cgtnfrancais/','')
            print(init_item['post_video_msg'])
            yield init_item