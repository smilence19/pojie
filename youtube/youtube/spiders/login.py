# -*- coding: utf-8 -*-
import scrapy
from scrapy import FormRequest
from selenium import webdriver
import os
import base64
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
from PIL import Image

class YoutubeVideosSpider(scrapy.Spider):
    name = 'login'
    allowed_domains = ['www.weibo.com']
    start_urls = [
        'https://weibo.com',
        #           'http://127.0.0.1:8050/info?wait=0.5&images=1&expand=1&timeout=90.0&url=https%3A%2F%2Fwww.youtube.com%2Fmy_videos%3Fo%3DU&lua_source=function+main%28splash%29%0D%0A++++splash.images_enabled+%3D+false%0D%0A++++splash%3Aon_request%28%0D%0A++++++++++++function%28request%29%0D%0A++++++++++++++++request%3Aset_header%28%27Cookie%27%2C%27PREF%3Df1%3D50000000%26f4%3D4000000%26f5%3D30%26al%3Dzh-CN%3B+_ga%3DGA1.2.1551080313.1519631749%3B+_gid%3DGA1.2.2107864435.1519631749%3B+LOGIN_INFO%3DAFmmF2swRAIga-UgsgOu93L7QY924vDoA9nf8S_TohHgl2_xIWMlsiwCIDZ3_yNPtZ-EU1mjQ22fiyBQr-eiOi_v-5psiqvl0Hl7%3AQUQ3MjNmelN3cDFHQkVUYnliVEl6bUEwbXh1eXh6SUhFOEI0UzdneXFlTlNDMVNYSnp5a3FCVEFvcV9kSEF6d0Q5aG50VnFnMno2UExqX3lTV3Z1NlYxZDlYR1dBTVVqbHFEdWdnbEJCV0JOZTdtSG9YVlo1eDVpYWNPd2Uyd1p1bmtsWV90R29xamlvakZIWWFOZFBrQTRmQlNlanJIcWZjaHFMOXBmQk5qVElVTXJvNGZNUmtDQllYc3d1cDJ1OHdCVmNhV2F2MFRxT2NKV3JWVENYQTh4Z3lzRWc4RlZaMDhFWmJxYlN2MnFfTjE2bmY0WWNFSQ%3D%3D%3B+APISID%3DCkD4QszXZD8TZUhA%2FAeO9cled_EL-9Hug_%3B+HSID%3DAtAiFrHalcv0TSlO2%3B+SAPISID%3DMgS2b-gUXC9kUQLs%2FAbIclDQc8r_M3c5To%3B+SID%3D0QWNn1dj70Lx9UnnP7fuR2sLUJOflNeBAf5Mo_KQ1wMLrMwSvuAN8IBESCTLCTCEos7t3A.%3B+SSID%3DApD50x2AlXSHSaz5E%3B+YSC%3Dk5jRk2PEUfE%3B+VISITOR_INFO1_LIVE%3DWQWqeYMqwiA%27%29%0D%0A++++++++++++end%29%0D%0A++%09splash%3Ago%28splash.args.url%29%0D%0A++%09splash%3Await%285%29%0D%0A++++return+%7B%0D%0A++++html+%3D+splash%3Ahtml%28%29%2C%0D%0A++++png+%3D+splash%3Apng%28%29%2C%0D%0A++++har+%3D+splash%3Ahar%28%29%2C%0D%0A++%7D%0D%0Aend']
        ]


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
            element = driver.find_element_by_xpath('//input[@id="loginname"]')
            if element.text == 'cctvfrench@126.com':
                print('账号已被记住！')
            else:
                element.send_keys('cctvfrench@126.com')  # 改成你的微博账号
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

    def login(self, response):
        formdata = {
        'email': '13810149762', 'password': 'flying555$'}
        yield FormRequest.from_response(response, formdata=formdata,callback = self.parse_login)

    def parse_login(self, response):
        print(response)

    def parse(self, response):

        print(response.text)
        f = open('test.png', 'wb')  # 若是'wb'就表示写二进制文件
        f.write(base64.b64decode(response.data['png']))
        f.close()

        pass
