# -*- coding: utf-8 -*-
import scrapy
from scrapy import FormRequest
from selenium import webdriver
import os
import base64
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
from PIL import Image
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


class YoutubeVideosSpider(scrapy.Spider):
    name = 'login_weixin'
    allowed_domains = ['mp.weixin.qq.com']
    start_urls = [
        'https://mp.weixin.qq.com',
        #           'http://127.0.0.1:8050/info?wait=0.5&images=1&expand=1&timeout=90.0&url=https%3A%2F%2Fwww.youtube.com%2Fmy_videos%3Fo%3DU&lua_source=function+main%28splash%29%0D%0A++++splash.images_enabled+%3D+false%0D%0A++++splash%3Aon_request%28%0D%0A++++++++++++function%28request%29%0D%0A++++++++++++++++request%3Aset_header%28%27Cookie%27%2C%27PREF%3Df1%3D50000000%26f4%3D4000000%26f5%3D30%26al%3Dzh-CN%3B+_ga%3DGA1.2.1551080313.1519631749%3B+_gid%3DGA1.2.2107864435.1519631749%3B+LOGIN_INFO%3DAFmmF2swRAIga-UgsgOu93L7QY924vDoA9nf8S_TohHgl2_xIWMlsiwCIDZ3_yNPtZ-EU1mjQ22fiyBQr-eiOi_v-5psiqvl0Hl7%3AQUQ3MjNmelN3cDFHQkVUYnliVEl6bUEwbXh1eXh6SUhFOEI0UzdneXFlTlNDMVNYSnp5a3FCVEFvcV9kSEF6d0Q5aG50VnFnMno2UExqX3lTV3Z1NlYxZDlYR1dBTVVqbHFEdWdnbEJCV0JOZTdtSG9YVlo1eDVpYWNPd2Uyd1p1bmtsWV90R29xamlvakZIWWFOZFBrQTRmQlNlanJIcWZjaHFMOXBmQk5qVElVTXJvNGZNUmtDQllYc3d1cDJ1OHdCVmNhV2F2MFRxT2NKV3JWVENYQTh4Z3lzRWc4RlZaMDhFWmJxYlN2MnFfTjE2bmY0WWNFSQ%3D%3D%3B+APISID%3DCkD4QszXZD8TZUhA%2FAeO9cled_EL-9Hug_%3B+HSID%3DAtAiFrHalcv0TSlO2%3B+SAPISID%3DMgS2b-gUXC9kUQLs%2FAbIclDQc8r_M3c5To%3B+SID%3D0QWNn1dj70Lx9UnnP7fuR2sLUJOflNeBAf5Mo_KQ1wMLrMwSvuAN8IBESCTLCTCEos7t3A.%3B+SSID%3DApD50x2AlXSHSaz5E%3B+YSC%3Dk5jRk2PEUfE%3B+VISITOR_INFO1_LIVE%3DWQWqeYMqwiA%27%29%0D%0A++++++++++++end%29%0D%0A++%09splash%3Ago%28splash.args.url%29%0D%0A++%09splash%3Await%285%29%0D%0A++++return+%7B%0D%0A++++html+%3D+splash%3Ahtml%28%29%2C%0D%0A++++png+%3D+splash%3Apng%28%29%2C%0D%0A++++har+%3D+splash%3Ahar%28%29%2C%0D%0A++%7D%0D%0Aend']
        ]

#     lua_script = """
#     function main(splash)
#         splash:on_request(
#             function(request)
#                 request:set_header('Cookie','_ga=GA1.2.1551080313.1519631749; _gid=GA1.2.2107864435.1519631749; PREF=f1=50000000&f4=4000000&f5=30&al=zh-CN; LOGIN_INFO=AFmmF2swRAIga-UgsgOu93L7QY924vDoA9nf8S_TohHgl2_xIWMlsiwCIDZ3_yNPtZ-EU1mjQ22fiyBQr-eiOi_v-5psiqvl0Hl7:QUQ3MjNmelN3cDFHQkVUYnliVEl6bUEwbXh1eXh6SUhFOEI0UzdneXFlTlNDMVNYSnp5a3FCVEFvcV9kSEF6d0Q5aG50VnFnMno2UExqX3lTV3Z1NlYxZDlYR1dBTVVqbHFEdWdnbEJCV0JOZTdtSG9YVlo1eDVpYWNPd2Uyd1p1bmtsWV90R29xamlvakZIWWFOZFBrQTRmQlNlanJIcWZjaHFMOXBmQk5qVElVTXJvNGZNUmtDQllYc3d1cDJ1OHdCVmNhV2F2MFRxT2NKV3JWVENYQTh4Z3lzRWc4RlZaMDhFWmJxYlN2MnFfTjE2bmY0WWNFSQ==; APISID=CkD4QszXZD8TZUhA/AeO9cled_EL-9Hug_; HSID=AtAiFrHalcv0TSlO2; SAPISID=MgS2b-gUXC9kUQLs/AbIclDQc8r_M3c5To; SID=0QWNn1dj70Lx9UnnP7fuR2sLUJOflNeBAf5Mo_KQ1wMLrMwSvuAN8IBESCTLCTCEos7t3A.; SSID=ApD50x2AlXSHSaz5E; YSC=k5jRk2PEUfE; VISITOR_INFO1_LIVE=WQWqeYMqwiA')
#             end)
#   	    splash:go(splash.args.url)
#   	    splash:wait(8)
#         return {
#         html = splash:html(),
#         png = splash:png(),
#         har = splash:har(),
#   }
# end
#     """
#
#     cookie = {'Cookie':'PREF=f1=50000000&f4=4000000&f5=30&al=zh-CN; _ga=GA1.2.1551080313.1519631749; _gid=GA1.2.2107864435.1519631749; LOGIN_INFO=AFmmF2swRAIga-UgsgOu93L7QY924vDoA9nf8S_TohHgl2_xIWMlsiwCIDZ3_yNPtZ-EU1mjQ22fiyBQr-eiOi_v-5psiqvl0Hl7:QUQ3MjNmelN3cDFHQkVUYnliVEl6bUEwbXh1eXh6SUhFOEI0UzdneXFlTlNDMVNYSnp5a3FCVEFvcV9kSEF6d0Q5aG50VnFnMno2UExqX3lTV3Z1NlYxZDlYR1dBTVVqbHFEdWdnbEJCV0JOZTdtSG9YVlo1eDVpYWNPd2Uyd1p1bmtsWV90R29xamlvakZIWWFOZFBrQTRmQlNlanJIcWZjaHFMOXBmQk5qVElVTXJvNGZNUmtDQllYc3d1cDJ1OHdCVmNhV2F2MFRxT2NKV3JWVENYQTh4Z3lzRWc4RlZaMDhFWmJxYlN2MnFfTjE2bmY0WWNFSQ==; APISID=CkD4QszXZD8TZUhA/AeO9cled_EL-9Hug_; HSID=AtAiFrHalcv0TSlO2; SAPISID=MgS2b-gUXC9kUQLs/AbIclDQc8r_M3c5To; SID=0QWNn1dj70Lx9UnnP7fuR2sLUJOflNeBAf5Mo_KQ1wMLrMwSvuAN8IBESCTLCTCEos7t3A.; SSID=ApD50x2AlXSHSaz5E; YSC=k5jRk2PEUfE; VISITOR_INFO1_LIVE=WQWqeYMqwiA'}
#     header = {
#         'Referer': 'https://www.youtube.com/my_videos?o=U',
#         'Content-Type': 'application/x-www-form-urlencoded',
#         'Host': 'www.youtube.com',
#         'Accept': '*/*',
#         'Connection': 'keep-alive',
#         'Accept-Language': 'zh-cn',
#         'Accept-Encoding': 'gzip, deflate',
#         'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0.3 Safari/604.5.6'
#     }

    # def start_requests(self):
    #     for url in self.start_urls:
    #         yield scrapy.Request(url=url, callback=self.parse,method='GET',cookies=self.cookie,headers=self.header)

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

        driver.get('https://mp.weixin.qq.com')
        driver.implicitly_wait(3)
        time.sleep(3)


        driver.save_screenshot('screen.png')

        try:
            driver.find_element_by_xpath('//input[@name="account"]').send_keys('cctvfrench@126.com')  # 改成你的微博账号
        except Exception as e:
            print(e)

        try:
            driver.find_element_by_xpath('//input[@name="password"]').send_keys(' i68507703')  # 改成你的微博密码
        except Exception as e:
            print(e)

        driver.save_screenshot('screen1.png')

        try:
            driver.find_element_by_css_selector('#header > div.banner > div > div > form > div.login_btn_panel > a').click()  # 点击登录
            driver.implicitly_wait(3)
            time.sleep(8)
        except Exception as e:
            print(e)

        driver.save_screenshot('screen2.png')

        try:
            element = driver.find_element_by_css_selector('#app > div.weui-desktop-layout__main__bd > div > div.js_scan.weui-desktop-qrcheck > div.weui-desktop-qrcheck__qrcode-area > div > img')
            img_url = element.get_attribute("src")
            print(img_url)


            if element:
                left = int(element.location['x'])
                top = int(element.location['y'])
                right = int(element.location['x'] + element.size['width'])
                bottom = int(element.location['y'] + element.size['height'])

                # 通过Image处理图像
                im = Image.open('screen2.png')
                im = im.crop((left, top, right, bottom))
                im.save('二维码.png')

                self.send()

                # sd_code = input("Please intput your code:")
                # print('验证码：' + sd_code)
                # driver.find_element_by_xpath('//input[@name="verifycode"]').send_keys(sd_code)  # 改成你的微博密码
                #
                # driver.find_element_by_css_selector(
                #     '#pl_login_form > div > div:nth-child(3) > div.info_list.login_btn > a > span').click()  # 点击登录
                # driver.implicitly_wait(3)
                # time.sleep(3)

        except Exception as e:
            print(e)



        # 获得 cookie信息
        driver.save_screenshot('screen3.png')

        cookie_list1 = driver.get_cookies()

        print(cookie_list1)

        # driver.get('https://weibo.com/p/1002062976971705/home?is_search=0&visible=0&is_all=1&is_tag=0&profile_ftype=1&page=1#feedtop')
        # driver.implicitly_wait(3)
        # time.sleep(6)

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

    def send(self):
        sender = 'huangqingjunqwe@126.com'
        receivers = '360999151@qq.com'
        message = MIMEMultipart('related')
        subject = '微信登陆二维码'
        message['Subject'] = subject
        message['From'] = sender
        message['To'] = receivers
        content = MIMEText('<html><body><img src="cid:imageid" alt="imageid"></body></html>', 'html', 'utf-8')
        message.attach(content)

        file = open("二维码.png", "rb")
        img_data = file.read()
        file.close()

        img = MIMEImage(img_data)
        img.add_header('Content-ID', 'imageid')
        message.attach(img)

        try:
            # server = smtplib.SMTP_SSL("smtp.qq.com", 465)
            server = smtplib.SMTP_SSL("smtp.126.com")
            server.login(sender, "123456qwe")
            server.sendmail(sender, receivers, message.as_string())
            server.quit()
            print("邮件发送成功")
        except smtplib.SMTPException as e:
            print(e)
    def parse_login(self, response):
        print(response)

    def parse(self, response):
        print(response.text)
        f = open('test.png', 'wb')  # 若是'wb'就表示写二进制文件
        f.write(base64.b64decode(response.data['png']))
        f.close()
        pass
