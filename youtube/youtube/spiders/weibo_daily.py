# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
import os
import base64
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
from PIL import Image
from scrapy_splash import SplashRequest
from youtube.items import WeiboItem,WeiboContentItem
import re,json
from scrapy.http import HtmlResponse

class YoutubeVideosSpider(scrapy.Spider):
    name = 'weibo_daily'
    allowed_domains = ['www.weibo.com']
    start_urls = [
        'https://weibo.com',
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
                    request:set_header('Cookie',splash.args.cookie)
        		end)
      	    splash:go(splash.args.url)
      	   wait_for_element(splash, "div.WB_h5video.hv-s1")
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
        'un': 'cctvfrench@126.com', 'ALF': '1552452298',
        'SCF': 'AqUxt-zwgcx-xh6WWZqDhbp380VclnRaud9WzRsxZnXfmc9l-hU-OFaBiUNga29U4kd68JwygboNUtOJzOY2GLc.',
        'SSOLoginState': '1520916299',
        'SUB': '_2A253oyccDeRhGeRH7FQY9y_LyzmIHXVU2R_UrDV8PUNbmtAKLXnskW9NTY0tPKDY5zSN5z4O-zH80zd5r6NAE-ts',
        'SUBP': '0033WrSXqPxfM725Ws9jqgMF55529P9D9WFIOGkBSqBgRJuB7T9OoCNj5JpX5K2hUgL.Foz4S0q4S02Neh-2dJLoIEyhxfx1i--ci-z0iK.fi--Ri-8si-82i--4i-2EiK.pi--4iKnpiK.0',
        'SUHB': '0P1c6vhOWVwRV_', 'Apache': '466189967384.2229.1520916287714',
        'ULV': '1520916287952:43:5:1:466189967384.2229.1520916287714:1520384878812', '_s_tentry': 'passport.weibo.com',
        'cross_origin_proto': 'SSL', 'login_sid_t': '2f6e353cfec6ac2a428b61101aade795', 'UOR': ',,www.baidu.com',
        'wvr': '6', 'SINAGLOBAL': '8119989025872.201.1459349736281', 'TC-Page-G0': 'e2379342ceb6c9c8726a496a5565689e',
        'TC-V5-G0': '1e4d14527a0d458a29b1435fb7d41cc3', 'WBStorage': 'c5ff51335af29d81|undefined',
        'TC-Ugrow-G0': '370f21725a3b0b57d0baaf8dd6f16a18'
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
    splash_cookie = ''

    def start_requests(self):
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = (
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0.3 Safari/604.5.6'
        )

        driver = webdriver.PhantomJS(desired_capabilities=dcap)
        driver.set_window_size(1920, 1080)

        if os.path.exists('cookie_list.txt'):
            fh = open('cookie_list.txt', 'r')
            cookie_txt_list = fh.readlines()
            fh.close()
            if len(cookie_txt_list):
                strr = cookie_txt_list[0].replace('"weibo.com"', '".weibo.com"').replace("'weibo.com'", "'.weibo.com'")
                print(strr)
                list = eval(strr)

                if len(list):
                    driver.get('https://www.weibo.com')
                    driver.delete_all_cookies()
                    for cookie in list:
                        print(cookie)
                        driver.add_cookie(cookie)
                        #driver.add_cookie({k: cookie[k] for k in ('name', 'value', 'domain', 'path','httponly','secure','expires','expiry')})
                    #driver.implicitly_wait(3)
                    #time.sleep(3)

        driver.get('https://www.weibo.com')
        driver.implicitly_wait(3)
        time.sleep(3)


        driver.save_screenshot('screen.png')

        try:
            driver.find_element_by_xpath('//input[@id="loginname"]').send_keys('cctvfrench@126.com')  # 改成你的微博账号
        except Exception as e:
            print(e)

        try:
            driver.find_element_by_xpath('//input[@type="password"]').send_keys('CGTNFnewmedia1')  # 改成你的微博密码
        except Exception as e:
            print(e)

        driver.save_screenshot('screen1.png')

        try:
            driver.find_element_by_css_selector('#pl_login_form > div > div:nth-child(3) > div.info_list.login_btn > a > span').click()  # 点击登录
            driver.implicitly_wait(3)
            time.sleep(3)
        except Exception as e:
            print(e)

        driver.save_screenshot('screen2.png')

        try:
            element = driver.find_element_by_xpath('//a[@class="code W_fl"]')
            if element:
                left = int(element.location['x'])
                top = int(element.location['y'])
                right = int(element.location['x'] + element.size['width'])
                bottom = int(element.location['y'] + element.size['height'])

                # 通过Image处理图像
                im = Image.open('screen2.png')
                im = im.crop((left, top, right, bottom))
                im.save('code.png')

                sd_code = input("Please intput your code:")
                print('验证码：' + sd_code)
                driver.find_element_by_xpath('//input[@name="verifycode"]').send_keys(sd_code)  # 改成你的微博密码

                driver.find_element_by_css_selector(
                    '#pl_login_form > div > div:nth-child(3) > div.info_list.login_btn > a > span').click()  # 点击登录
                driver.implicitly_wait(3)
                time.sleep(3)

        except Exception as e:
            print(e)



        # 获得 cookie信息
        driver.save_screenshot('screen3.png')

        cookie_list1 = driver.get_cookies()

        print(cookie_list1)
        driver.get('https://weibo.com/p/1002062976971705/home?is_search=0&visible=0&is_all=1&is_tag=0&profile_ftype=1&page=1#feedtop')
        driver.implicitly_wait(3)
        time.sleep(6)

        driver.save_screenshot('screen4.png')

        cookie_list = driver.get_cookies()
        print (cookie_list)
        cookie_dict = {}
        for item in cookie_list:
            cookie_dict[item['name']] = item['value']

        print(cookie_dict)

        fh = open('cookie_dict.txt', 'w')
        fh.write(str(cookie_dict))
        fh.close()

        fh = open('cookie_list.txt', 'w')
        fh.write(str(cookie_list))
        fh.close()

        driver.quit()


#开始爬取工作
        if os.path.exists('cookie_dict.txt'):
            fh = open('cookie_dict.txt', 'r')
            cookie_txt_list = fh.readlines()
            if len(cookie_txt_list):
                cookie = cookie_txt_list[0]
                print(cookie)
                self.cookie = eval(cookie)
                splash_cookie = cookie.replace("': '",'=').replace("', '",';').replace(", '",";").replace("{'","").replace("'}",'')
                self.splash_cookie = splash_cookie
                print(splash_cookie)
            fh.close()


        for url in self.start_urls:
            yield SplashRequest(url=url, callback=self.parse,
                                args={'wait': 0.5,
                                      'png':1,
                                      'html':1,
                                      'cookie':self.splash_cookie,
                                      'lua_source': self.lua_script,
                                      }, endpoint='execute')

    def parse(self, response):


        f = open('test.png', 'wb')  # 若是'wb'就表示写二进制文件
        f.write(base64.b64decode(response.data['png']))
        f.close()

        list = response.xpath("//div[@class = 'WB_feed WB_feed_v3 WB_feed_v4']/div")

        for item in list:
            # print(item)
            print(item.xpath("./@mid").extract())
            mid_list = item.xpath("./@mid").extract()
            if len(mid_list):
                init_item = WeiboItem()
                # id
                init_item['post_id'] = mid_list[0]

                # 获取贴文
                msg_list = item.xpath(".//div[@class = 'WB_text W_f14']").extract()
                a_list = item.xpath(".//div[@class = 'WB_text W_f14']/a/text()").extract()

                if '展开全文' in a_list:
                    # 获取全部内容
                    content_url = 'https://weibo.com/p/aj/mblog/getlongtext?ajwvr=6&mid=' + init_item[
                        'post_id'] + '&is_settop&is_sethot&is_setfanstop&is_setyoudao&__rnd=' + str(
                        int(time.time() * 1000))
                    yield scrapy.Request(
                        url=content_url,
                        callback=self.content_parse, method='GET', cookies=self.cookie, dont_filter=True)
                dr = re.compile(r'<[^>]+>', re.S)
                msg = dr.sub('', msg_list[0])
                init_item['post_message'] = msg.replace('\n', '').replace("   ", "")

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
                count = item.xpath(".//ul/li")
                if len(count) >3 :
                    # 阅读量
                    watch_list = item.xpath(".//ul/li[1]/a/span/span/i/@title").extract()
                    if len(watch_list):
                        init_item['post_watch_times'] = watch_list[0].replace('此条微博已经被阅读', '').replace('次', '')
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
                else:
                    # 阅读量
                    watch_list = item.xpath(".//ul/li[1]/a/span/span/i/@title").extract()
                    if len(watch_list):
                        init_item['post_watch_times'] = watch_list[0].replace('此条微博已经被阅读', '').replace('次', '')
                    # 转发
                    init_item['post_shares_times'] = 0

                    # 评论
                    comments_list = item.xpath(".//ul/li[2]/a/span/span/span/em[2]/text()").extract()
                    if '评论' in comments_list:
                        init_item['post_comments_times'] = 0
                    else:
                        init_item['post_comments_times'] = comments_list[0]

                    # 点赞
                    like_list = item.xpath(".//ul/li[3]/a/span/span/span/em[2]/text()").extract()
                    if '赞' in like_list:
                        init_item['post_likes_times'] = 0
                    else:
                        if len(like_list):
                            init_item['post_likes_times'] = like_list[0]
                        else:
                            init_item['post_likes_times'] = 0

                # 观看量
                play_list = item.xpath(".//div[@class = 'WB_h5video hv-s1']")
                if len(play_list) > 0:
                    play_list = play_list[0].xpath(
                        "./div[@class = 'con-4']/div[@class = 'opt hv-pos hv-center']/div")
                    if len(play_list) > 0:
                        play_times_list = play_list[0].xpath('./text()').extract()
                        if len(play_times_list):
                            init_item['post_play_times'] = play_times_list[0].replace('次播放', '')
                            if (init_item['post_play_times']).find('万') > -1:
                                init_item['post_play_times'] = float(
                                    init_item['post_play_times'].replace("万", '')) * 10000
                        else:
                            init_item['post_play_times'] = 0
                        video_duration_list = play_list[1].xpath('./text()').extract()
                        if len(video_duration_list):
                            init_item['post_video_duration'] = video_duration_list[0]
                        else:
                            init_item['post_video_duration'] = ''
                else:

                    play_list = item.xpath(".//ul[@class = 'WB_media_a WB_media_a_m1 clearfix']/li/div[1]/span")
                    if len(play_list):
                        play_times_list = play_list[0].xpath('./text()').extract()
                        if len(play_times_list):
                            init_item['post_play_times'] = play_times_list[0].replace('次播放', '').replace('次观看', '')
                            if (init_item['post_play_times']).find('万') > -1:
                                init_item['post_play_times'] = float(init_item['post_play_times'].replace("万",'')) * 10000
                        else:
                            init_item['post_play_times'] = 0
                        video_duration_list = play_list[0].xpath('./span/text()').extract()
                        if len(video_duration_list):
                            init_item['post_video_duration'] = video_duration_list[0]
                        else:
                            init_item['post_video_duration'] = ''

                    else:
                        play_a = item.xpath(".//ul[@class = 'WB_media_a WB_media_a_m1 clearfix']/li/@action-data").extract()
                        if len(play_a):
                            pp = re.compile(r'play_count=(.*?)&')
                            matcher1 = re.search(pp, play_a[0])
                            if matcher1:
                                init_item['post_play_times']  = matcher1.group(1)
                            else:
                                init_item['post_play_times'] = 0

                            p2 = re.compile(r'duration=(.*?)&')
                            matcher2 = re.search(p2, play_a[0])
                            if matcher2:
                                seconds = matcher2.group(1)
                                index = seconds.find('.')
                                seconds = int(seconds)
                                if index > -1:
                                    seconds = seconds[:index]
                                init_item['post_video_duration'] = str(int(seconds / 60)) +":"+str(seconds%60)
                            else:
                                init_item['post_video_duration'] = 0
                        else:
                            init_item['post_play_times'] = 0
                            init_item['post_video_duration'] = ''

                if init_item['post_shares_times'] =='评论':
                    init_item['post_shares_times'] = 0
                yield init_item

        if len(list):
            print(str(time.time()))
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
            yield scrapy.Request(
                url='https://weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&domain=100206&profile_ftype=1&is_all=1&pagebar=0&pl_name=Pl_Official_MyProfileFeed__28&id=1002062976971705&script_uri=/p/1002062976971705/home&feed_type=0&page=' + result + '&pre_page=' + result + '&domain_op=100206&__rnd=' + str(
                    time.time()),
                callback=self.list_parse, method='GET', cookies=self.cookie)
        pass

    def list_parse(self, response):
        # print(response.text)

        ajson = json.loads(response.text)
        data = ajson['data']

        aresponse = HtmlResponse(url=response.url, body=data, encoding='utf-8')

        list = aresponse.xpath("//div[@class = 'WB_cardwrap WB_feed_type S_bg2 WB_feed_like ']")
        if len(list) == 0:
            list = aresponse.xpath("//div[@class = 'WB_cardwrap WB_feed_type S_bg2 WB_feed_vipcover WB_feed_like ']")
        for item in list:
            # print(item)
            print(item.xpath("./@mid").extract())
            mid_list = item.xpath("./@mid").extract()
            if len(mid_list):
                init_item = WeiboItem()
                # id
                init_item['post_id'] = mid_list[0]

                # 获取贴文
                msg_list = item.xpath(".//div[@class = 'WB_text W_f14']").extract()
                a_list = item.xpath(".//div[@class = 'WB_text W_f14']/a/text()").extract()

                if '展开全文' in a_list:
                    # 获取全部内容
                    content_url = 'https://weibo.com/p/aj/mblog/getlongtext?ajwvr=6&mid=' + init_item[
                        'post_id'] + '&is_settop&is_sethot&is_setfanstop&is_setyoudao&__rnd=' + str(
                        int(time.time() * 1000))
                    yield scrapy.Request(
                        url=content_url,
                        callback=self.content_parse, method='GET', cookies=self.cookie, dont_filter=True)
                dr = re.compile(r'<[^>]+>', re.S)
                msg = dr.sub('', msg_list[0])
                init_item['post_message'] = msg.replace('\n', '').replace("   ", "")

                # url地址
                url_list = item.xpath(".//div[@class = 'WB_text W_f14']/a[@class = 'WB_text_opt']/@href").extract()
                if len(url_list):
                    init_item['post_url'] = 'https:' + url_list[0]
                else:
                    url_list = item.xpath(".//div[@class = 'WB_from S_txt2']/a[1]/@href").extract()
                    if len(url_list):
                        init_item['post_url'] = 'https://www.weibo.com' + url_list[0]
                    else:
                        init_item['post_url'] = ''
                # 日期
                date_list = item.xpath(".//div[@class = 'WB_from S_txt2']/a[1]/@title").extract()
                if len(date_list):
                    init_item['post_create_time'] = date_list[0]
                count = item.xpath(".//ul/li")
                if len(count) > 3:
                    # 阅读量
                    watch_list = item.xpath(".//ul/li[1]/a/span/span/i/@title").extract()
                    if len(watch_list):
                        init_item['post_watch_times'] = watch_list[0].replace('此条微博已经被阅读', '').replace('次', '')
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
                else:
                    # 阅读量
                    watch_list = item.xpath(".//ul/li[1]/a/span/span/i/@title").extract()
                    if len(watch_list):
                        init_item['post_watch_times'] = watch_list[0].replace('此条微博已经被阅读', '').replace('次', '')
                    # 转发
                    init_item['post_shares_times'] = 0

                    # 评论
                    comments_list = item.xpath(".//ul/li[2]/a/span/span/span/em[2]/text()").extract()
                    if '评论' in comments_list:
                        init_item['post_comments_times'] = 0
                    else:
                        init_item['post_comments_times'] = comments_list[0]

                    # 点赞
                    like_list = item.xpath(".//ul/li[3]/a/span/span/span/em[2]/text()").extract()
                    if '赞' in like_list:
                        init_item['post_likes_times'] = 0
                    else:
                        if len(like_list):
                            init_item['post_likes_times'] = like_list[0]
                        else:
                            init_item['post_likes_times'] = 0
                # 观看量
                play_list = item.xpath(".//div[@class = 'WB_h5video hv-s1']")
                if init_item['post_id'] == '4029051612058137':
                    print(item.extract())

                if len(play_list) > 0:
                    play_list = play_list[0].xpath(
                                "./div[@class = 'con-4']/div[@class = 'opt hv-pos hv-center']/div")
                    if len(play_list) > 0:
                        play_times_list = play_list[0].xpath('./text()').extract()
                        if len(play_times_list):
                            init_item['post_play_times'] = play_times_list[0].replace('次播放', '')
                            if (init_item['post_play_times']).find('万')>-1:
                                init_item['post_play_times'] = float(
                                    init_item['post_play_times'].replace("万", '')) * 10000

                        else:
                            init_item['post_play_times'] = 0
                        video_duration_list = play_list[1].xpath('./text()').extract()
                        if len(video_duration_list):
                            init_item['post_video_duration'] = video_duration_list[0]
                        else:
                            init_item['post_video_duration'] = ''

                else:

                    play_list = item.xpath(".//ul[@class = 'WB_media_a WB_media_a_m1 clearfix']/li/div[1]/span")
                    if len(play_list):
                        play_times_list = play_list[0].xpath('./text()').extract()
                        if len(play_times_list):
                            init_item['post_play_times'] = play_times_list[0].replace('次播放', '').replace('次观看', '')
                            if (init_item['post_play_times']).find('万')>-1:
                                init_item['post_play_times'] = float(
                                    init_item['post_play_times'].replace("万", '')) * 10000
                        else:
                            init_item['post_play_times'] = 0
                        video_duration_list = play_list[0].xpath('./span/text()').extract()
                        if len(video_duration_list):
                            init_item['post_video_duration'] = video_duration_list[0]
                        else:
                            init_item['post_video_duration'] = ''

                    else:
                        play_a = item.xpath(
                            ".//ul[@class = 'WB_media_a WB_media_a_m1 clearfix']/li/@action-data").extract()
                        if len(play_a):
                            pp = re.compile(r'play_count=(.*?)&')
                            matcher1 = re.search(pp, play_a[0])
                            if matcher1:
                                init_item['post_play_times'] = matcher1.group(1)
                            else:
                                init_item['post_play_times'] = 0

                            p2 = re.compile(r'duration=(.*?)&')
                            matcher2 = re.search(p2, play_a[0])
                            if matcher2:
                                seconds = matcher2.group(1)
                                index = seconds.find('.')
                                if index > -1:
                                    seconds = seconds[:index]
                                seconds = int(seconds)

                                init_item['post_video_duration'] = str(int(seconds / 60)) + ":" + str(seconds % 60)
                            else:
                                init_item['post_video_duration'] = ''
                        else:
                            init_item['post_play_times'] = 0
                            init_item['post_video_duration'] = ''



                if init_item['post_shares_times'] =='评论':
                    init_item['post_shares_times'] = 0
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

        if 'pagebar=1' in response.url and int(result)<=3:
            yield SplashRequest(url="https://weibo.com/p/1002062976971705/home?is_search=0&visible=0&is_all=1&is_tag=0&profile_ftype=1&page="+str(int(result)+1)+"#feedtop", callback=self.parse,
                                args={'wait': 0.5,
                                      'png': 1,
                                      'html': 1,
                                      'cookie': self.splash_cookie,
                                      'lua_source': self.lua_script,
                                      }, endpoint='execute',

                                )
        else:
            yield scrapy.Request(
                url='https://weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&domain=100206&profile_ftype=1&is_all=1&pagebar=1&pl_name=Pl_Official_MyProfileFeed__28&id=1002062976971705&script_uri=/p/1002062976971705/home&feed_type=0&page='+result+'&pre_page='+result+'&domain_op=100206&__rnd=' + str(
                    time.time()),
                callback=self.list_parse, method='GET', cookies=self.cookie)

    def content_parse(self, response):

        ajson = json.loads(response.text)

        if 'html' in ajson:
            data = ajson['data']['html']
            dr = re.compile(r'<[^>]+>', re.S)
            msg = dr.sub('', data)
            if len(msg):
                msg = msg.replace('\n', '').replace("   ", "")
                print(msg)
            p = re.compile(r'&mid=(.*?)&')
            matcher1 = re.search(p, response.url)
            mid = ''
            if matcher1:
                mid = matcher1.group(1)

            ainit_item = WeiboContentItem()
            ainit_item['post_id'] = mid
            ainit_item['post_message'] = msg
            yield ainit_item
        else:
            print("ERROR  "+ajson)