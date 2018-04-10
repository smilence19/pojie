# -*- coding: utf-8 -*-
import scrapy
from scrapy import FormRequest
from selenium import webdriver
import os
import base64
from scrapy_splash import SplashRequest
"""function wait_for_element(splash, css, maxwait)
  -- Wait until a selector matches an element
  -- in the page. Return an error if waited more
  -- than maxwait seconds.
  if maxwait == nil then
      maxwait = 10
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
        splash:set_user_agent("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0.3 Safari/604.5.6")   
  	    splash:go(splash.args.url)
  	    splash:wait(8)
  	    splash:set_viewport_full()
  	    local loginname = splash:select('#loginname')
  	    assert(loginname:mouse_hover{x=0, y=0})
        loginname:send_text('login_splash.py')
        
        assert(splash:wait(0))
        local loginname1 = splash:select('#pl_login_form > div > div:nth-child(3) > div.info_list.password > div > input')
  	    assert(loginname1:mouse_hover{x=0, y=0})
        loginname1:send_text('super2222')
        assert(splash:wait(1))
        local btn = splash:select('#pl_login_form > div > div:nth-child(3) > div.info_list.login_btn > a > span')
        assert(btn:mouse_hover{x=0, y=0})
        btn:mouse_click()
        
        assert(splash:wait(7))
        splash:wait(7)
  		# wait_for_element(splash, "#pl_common_top > div > div > div.gn_position > div.gn_set.S_line1 > div:nth-child(1) > a > em.W_ficon.ficon_mail.S_ficon")
        return {
        html = splash:html(),
        png = splash:png(),
        har = splash:har(),
  }
end"""

class YoutubeVideosSpider(scrapy.Spider):
    name = 'twitter_login_splash'
    allowed_domains = ['twitter.com']
    start_urls = [
        'https://twitter.com',
        #           'http://127.0.0.1:8050/info?wait=0.5&images=1&expand=1&timeout=90.0&url=https%3A%2F%2Fwww.youtube.com%2Fmy_videos%3Fo%3DU&lua_source=function+main%28splash%29%0D%0A++++splash.images_enabled+%3D+false%0D%0A++++splash%3Aon_request%28%0D%0A++++++++++++function%28request%29%0D%0A++++++++++++++++request%3Aset_header%28%27Cookie%27%2C%27PREF%3Df1%3D50000000%26f4%3D4000000%26f5%3D30%26al%3Dzh-CN%3B+_ga%3DGA1.2.1551080313.1519631749%3B+_gid%3DGA1.2.2107864435.1519631749%3B+LOGIN_INFO%3DAFmmF2swRAIga-UgsgOu93L7QY924vDoA9nf8S_TohHgl2_xIWMlsiwCIDZ3_yNPtZ-EU1mjQ22fiyBQr-eiOi_v-5psiqvl0Hl7%3AQUQ3MjNmelN3cDFHQkVUYnliVEl6bUEwbXh1eXh6SUhFOEI0UzdneXFlTlNDMVNYSnp5a3FCVEFvcV9kSEF6d0Q5aG50VnFnMno2UExqX3lTV3Z1NlYxZDlYR1dBTVVqbHFEdWdnbEJCV0JOZTdtSG9YVlo1eDVpYWNPd2Uyd1p1bmtsWV90R29xamlvakZIWWFOZFBrQTRmQlNlanJIcWZjaHFMOXBmQk5qVElVTXJvNGZNUmtDQllYc3d1cDJ1OHdCVmNhV2F2MFRxT2NKV3JWVENYQTh4Z3lzRWc4RlZaMDhFWmJxYlN2MnFfTjE2bmY0WWNFSQ%3D%3D%3B+APISID%3DCkD4QszXZD8TZUhA%2FAeO9cled_EL-9Hug_%3B+HSID%3DAtAiFrHalcv0TSlO2%3B+SAPISID%3DMgS2b-gUXC9kUQLs%2FAbIclDQc8r_M3c5To%3B+SID%3D0QWNn1dj70Lx9UnnP7fuR2sLUJOflNeBAf5Mo_KQ1wMLrMwSvuAN8IBESCTLCTCEos7t3A.%3B+SSID%3DApD50x2AlXSHSaz5E%3B+YSC%3Dk5jRk2PEUfE%3B+VISITOR_INFO1_LIVE%3DWQWqeYMqwiA%27%29%0D%0A++++++++++++end%29%0D%0A++%09splash%3Ago%28splash.args.url%29%0D%0A++%09splash%3Await%285%29%0D%0A++++return+%7B%0D%0A++++html+%3D+splash%3Ahtml%28%29%2C%0D%0A++++png+%3D+splash%3Apng%28%29%2C%0D%0A++++har+%3D+splash%3Ahar%28%29%2C%0D%0A++%7D%0D%0Aend']
        ]

    lua_script = """
        function main(splash)
        splash:set_user_agent("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0.3 Safari/604.5.6")   
  	    splash:go(splash.args.url)
  	    splash:wait(8)
  	    splash:set_viewport_full()
  	    local loginname = splash:select('#doc > div > div.StaticLoggedOutHomePage-content > div.StaticLoggedOutHomePage-cell.StaticLoggedOutHomePage-utilityBlock > div.StaticLoggedOutHomePage-login > form > div.LoginForm-input.LoginForm-username > input')
  	    assert(loginname:mouse_hover{x=0, y=0})
        loginname:send_text('cgtnfnewmedia@126.com')
        
        assert(splash:wait(0))
        local loginname1 = splash:select('#doc > div > div.StaticLoggedOutHomePage-content > div.StaticLoggedOutHomePage-cell.StaticLoggedOutHomePage-utilityBlock > div.StaticLoggedOutHomePage-login > form > div.LoginForm-input.LoginForm-password > input')
  	    assert(loginname1:mouse_hover{x=0, y=0})
        loginname1:send_text('francophone00358')
        --assert(splash:wait(1))
        local btn = splash:select('#doc > div > div.StaticLoggedOutHomePage-content > div.StaticLoggedOutHomePage-cell.StaticLoggedOutHomePage-utilityBlock > div.StaticLoggedOutHomePage-login > form > input.EdgeButton.EdgeButton--secondary.EdgeButton--medium.submit.js-submit')
        assert(btn:mouse_hover{x=0, y=0})
        btn:mouse_click()
        
        assert(splash:wait(7))
        splash:wait(7)
        
        return {
        html = splash:html(),
        png = splash:png(),
        har = splash:har(),
        cookie = splash:get_cookies()
        
    
  }
end
    """
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
        for url in self.start_urls:
            yield SplashRequest(url=url, callback=self.parse,
                                args={'wait': 0.5,
                                      'png':1,
                                      'html':1,
                                      'lua_source': self.lua_script,
                                      }, endpoint='execute')



    def parse(self, response):

        f = open('test.png', 'wb')  # 若是'wb'就表示写二进制文件
        f.write(base64.b64decode(response.data['png']))
        f.close()

        cookie_list = response.data['cookie']
        print(cookie_list)
        cookie_dict = {}
        for item in cookie_list:
            print(item)
            cookie_dict[item['name']] = item['value']



        fh = open('twitter_cookie_dict.txt', 'w')
        fh.write(str(cookie_dict))
        fh.close()

        fh = open('twitter_cookie_list.txt', 'w')
        fh.write(str(cookie_list))
        fh.close()

        pass
