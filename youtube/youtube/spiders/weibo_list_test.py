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
    name = 'weibo_list_test'
    allowed_domains = ['weibo.com']
    start_urls = [
        'https://weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&domain=100206&profile_ftype=1&is_all=1&pagebar=1&pl_name=Pl_Official_MyProfileFeed__28&id=1002062976971705&script_uri=/p/1002062976971705/home&feed_type=0&page=74&pre_page=74&domain_op=100206&__rnd=1519889526.553851',
        #           'http://127.0.0.1:8050/info?wait=0.5&images=1&expand=1&timeout=90.0&url=https%3A%2F%2Fwww.youtube.com%2Fmy_videos%3Fo%3DU&lua_source=function+main%28splash%29%0D%0A++++splash.images_enabled+%3D+false%0D%0A++++splash%3Aon_request%28%0D%0A++++++++++++function%28request%29%0D%0A++++++++++++++++request%3Aset_header%28%27Cookie%27%2C%27PREF%3Df1%3D50000000%26f4%3D4000000%26f5%3D30%26al%3Dzh-CN%3B+_ga%3DGA1.2.1551080313.1519631749%3B+_gid%3DGA1.2.2107864435.1519631749%3B+LOGIN_INFO%3DAFmmF2swRAIga-UgsgOu93L7QY924vDoA9nf8S_TohHgl2_xIWMlsiwCIDZ3_yNPtZ-EU1mjQ22fiyBQr-eiOi_v-5psiqvl0Hl7%3AQUQ3MjNmelN3cDFHQkVUYnliVEl6bUEwbXh1eXh6SUhFOEI0UzdneXFlTlNDMVNYSnp5a3FCVEFvcV9kSEF6d0Q5aG50VnFnMno2UExqX3lTV3Z1NlYxZDlYR1dBTVVqbHFEdWdnbEJCV0JOZTdtSG9YVlo1eDVpYWNPd2Uyd1p1bmtsWV90R29xamlvakZIWWFOZFBrQTRmQlNlanJIcWZjaHFMOXBmQk5qVElVTXJvNGZNUmtDQllYc3d1cDJ1OHdCVmNhV2F2MFRxT2NKV3JWVENYQTh4Z3lzRWc4RlZaMDhFWmJxYlN2MnFfTjE2bmY0WWNFSQ%3D%3D%3B+APISID%3DCkD4QszXZD8TZUhA%2FAeO9cled_EL-9Hug_%3B+HSID%3DAtAiFrHalcv0TSlO2%3B+SAPISID%3DMgS2b-gUXC9kUQLs%2FAbIclDQc8r_M3c5To%3B+SID%3D0QWNn1dj70Lx9UnnP7fuR2sLUJOflNeBAf5Mo_KQ1wMLrMwSvuAN8IBESCTLCTCEos7t3A.%3B+SSID%3DApD50x2AlXSHSaz5E%3B+YSC%3Dk5jRk2PEUfE%3B+VISITOR_INFO1_LIVE%3DWQWqeYMqwiA%27%29%0D%0A++++++++++++end%29%0D%0A++%09splash%3Ago%28splash.args.url%29%0D%0A++%09splash%3Await%285%29%0D%0A++++return+%7B%0D%0A++++html+%3D+splash%3Ahtml%28%29%2C%0D%0A++++png+%3D+splash%3Apng%28%29%2C%0D%0A++++har+%3D+splash%3Ahar%28%29%2C%0D%0A++%7D%0D%0Aend']
        ]

    lua_script = """
      function main(splash)
        splash:on_request(
            function(request)
                request:set_header('Cookie','ALF=1551405463; SCF=AqUxt-zwgcx-xh6WWZqDhbp380VclnRaud9WzRsxZnXfgg3Je7jFcGUlYkzigxi1kjHo8_X-Co92njPfXoeybLg.; SUB=_2A253ky5JDeRhGeRH7FQY9y_LyzmIHXVU6RiBrDV8PUNbmtANLRjikW9NTY0tPGT4qL2s-wp1Ri7nfRLh0LJuUlmi; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFIOGkBSqBgRJuB7T9OoCNj5JpX5KMhUgL.Foz4S0q4S02Neh-2dJLoIEyhxfx1i--ci-z0iK.fi--Ri-8si-82i--4i-2EiK.pi--4iKnpiK.0; SUHB=0vJYda9BnMhRHT; UOR=,,www.webbaozi.com; SSOLoginState=1519719405; wvr=6; un=cctvfrench@126.com; Apache=8953999087365.436.1519632234197; ULV=1519632234204:38:2:1:8953999087365.436.1519632234197:1519132374649; _s_tentry=www.baidu.com; cross_origin_proto=SSL; login_sid_t=be16f39e233ee88d68d1ca2011523eef; SINAGLOBAL=8119989025872.201.1459349736281; TC-Page-G0=42b289d444da48cb9b2b9033b1f878d9; YF-V5-G0=cd5d86283b86b0d506628aedd6f8896e; YF-Page-G0=b9385a03a044baf8db46b84f3ff125a0; YF-Ugrow-G0=169004153682ef91866609488943c77f; TC-Ugrow-G0=968b70b7bcdc28ac97c8130dd353b55e; TC-V5-G0=866fef700b11606a930f0b3297300d95')
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
        'ALF':'1551405463','SCF':'AqUxt-zwgcx-xh6WWZqDhbp380VclnRaud9WzRsxZnXfgg3Je7jFcGUlYkzigxi1kjHo8_X-Co92njPfXoeybLg.','SUB':'_2A253ky5JDeRhGeRH7FQY9y_LyzmIHXVU6RiBrDV8PUNbmtANLRjikW9NTY0tPGT4qL2s-wp1Ri7nfRLh0LJuUlmi','SUBP':'0033WrSXqPxfM725Ws9jqgMF55529P9D9WFIOGkBSqBgRJuB7T9OoCNj5JpX5KMhUgL.Foz4S0q4S02Neh-2dJLoIEyhxfx1i--ci-z0iK.fi--Ri-8si-82i--4i-2EiK.pi--4iKnpiK.0','SUHB':'0vJYda9BnMhRHT','UOR':',,www.webbaozi.com','SSOLoginState':'1519719405','wvr':'6','un':'cctvfrench@126.com','Apache':'8953999087365.436.1519632234197','ULV':'1519632234204:38:2:1:8953999087365.436.1519632234197:1519132374649','_s_tentry':'www.baidu.com','cross_origin_proto':'SSL','login_sid_t':'be16f39e233ee88d68d1ca2011523eef','SINAGLOBAL':'8119989025872.201.1459349736281','TC-Page-G0':'42b289d444da48cb9b2b9033b1f878d9','YF-V5-G0':'cd5d86283b86b0d506628aedd6f8896e','YF-Page-G0':'b9385a03a044baf8db46b84f3ff125a0','YF-Ugrow-G0':'169004153682ef91866609488943c77f','TC-Ugrow-G0':'968b70b7bcdc28ac97c8130dd353b55e','TC-V5-G0':'866fef700b11606a930f0b3297300d95'
    }
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

    # def start_requests(self):
    #     for url in self.start_urls:
    #         yield scrapy.Request(url=url, callback=self.parse,method='GET',cookies=self.cookie,headers=self.header)



    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url= 'https://weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&domain=100206&profile_ftype=1&is_all=1&pagebar=1&pl_name=Pl_Official_MyProfileFeed__28&id=1002062976971705&script_uri=/p/1002062976971705/home&feed_type=0&page=74&pre_page=74&domain_op=100206&__rnd=1519889526.553851',
                callback=self.parse, method='GET', cookies=self.cookie)
    def parse(self, response):
        # print(response.text)

        ajson = json.loads(response.text)
        data = ajson['data']
        aresponse = HtmlResponse(url=response.url, body=data,encoding='utf-8')

        list = aresponse.xpath("//div[@class = 'WB_cardwrap WB_feed_type S_bg2 WB_feed_like ']")
        for item in list:
            # print(item)
            print(item.xpath("./@mid").extract())
            mid_list = item.xpath("./@mid").extract()
            if len(mid_list):
                init_item = WeiboItem()
                # id
                init_item['post_id'] = mid_list[0]
                msg_list = item.xpath(".//div[@class = 'WB_text W_f14']/text()").extract()
                if len(msg_list):
                    init_item['post_message'] = "".join(msg_list).replace('\n','').replace(" ","")
                # url地址
                url_list = item.xpath(".//div[@class = 'WB_text W_f14']/a[@class = 'WB_text_opt']/@href").extract()
                if len(url_list):
                    init_item['post_url'] = 'https:'+ url_list[0]
                else:
                    url_list = item.xpath(".//div[@class = 'WB_from S_txt2']/a[1]/@href").extract()
                    if len(url_list):
                        init_item['post_url'] = 'https://www.weibo.com' + url_list[0]
                    else:
                        init_item['post_url'] = ''
                # 日期
                date_list = item.xpath(".//div[@class = 'WB_from S_txt2']/a[1]/@title").extract()
                if len(date_list):
                    init_item['post_create_time'] =  date_list[0]
                # 阅读量
                watch_list = item.xpath(".//ul/li[1]/a/span/span/i/@title").extract()
                if len(watch_list):
                    init_item['post_watch_times'] = watch_list[0].replace('此条微博已经被阅读','').replace('次','')
                # 转发
                share_list = item.xpath(".//ul/li[2]/a/span/span/span/em[2]/text()").extract()
                if '转发' in share_list:
                    init_item['post_shares_times'] = 0
                else:
                    init_item['post_shares_times'] = share_list[0]

                # 评论
                comments_list = item.xpath(".//ul/li[3]/a/span/span/span/em[2]/text()").extract()
                if '评论' in comments_list:
                    init_item['post_comments_times'] = 0
                else:
                    init_item['post_comments_times'] = comments_list[0]

                # 点赞
                like_list = item.xpath(".//ul/li[4]/a/span/span/span/em[2]/text()").extract()
                if '赞' in like_list:
                    init_item['post_likes_times'] = 0
                else:
                    if len(like_list):
                        init_item['post_likes_times'] = like_list[0]
                    else:
                        init_item['post_likes_times'] = 0

                yield init_item

        p = re.compile(r'&page=(.*?)&')
        matcher1 = re.search(p, response.url)
        result = ''
        if matcher1:
            result = matcher1.group(1)
        else:
            p = re.compile(r'&page=(.*?)#')
            matcher2 = re.search(p, response.url)
            if matcher2:
                result = matcher2.group(1)

        if 'pagebar=1' in response.url:
            yield SplashRequest(url="https://weibo.com/p/1002062976971705/home?is_search=0&visible=0&is_all=1&is_tag=0&profile_ftype=1&page="+str(int(result)+1)+"#feedtop", callback=self.parse,
                                args={'wait': 0.5,
                                      'png': 1,
                                      'html': 1,
                                      'lua_source': self.lua_script,
                                      }, endpoint='execute',

                                )
        else:
            yield scrapy.Request(
                url='https://weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&domain=100206&profile_ftype=1&is_all=1&pagebar=1&pl_name=Pl_Official_MyProfileFeed__28&id=1002062976971705&script_uri=/p/1002062976971705/home&feed_type=0&page='+result+'&pre_page='+result+'&domain_op=100206&__rnd=' + str(
                    time.time()),
                callback=self.parse, method='GET', cookies=self.cookie)


