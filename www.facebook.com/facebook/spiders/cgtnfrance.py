# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
import json
from facebook.items import FacebookPosts


PROXY = """
function main(splash)
    splash.images_enabled = false
    splash:on_request(
            function(request)
                request:set_header('Cookie','presence=EDvF3EtimeF1516851291EuserFA21B22221132390A2EstateFDutF1516851291482CEchFDp_5f1B22221132390F2CC; wd=1181x674; dpr=2; act=1516848972797%2F5; c_user=100022221132390; fr=07gv1HLksbxE7qXJL.AWVYwYeEga6K47j5ZmOSIRPDCig.BZy1j0.xE.Fpl.0.0.BaaUbQ.AWWKTRfF; xs=39%3Am__JJZZOSY6Sxg%3A2%3A1516764670%3A11335%3A8671; datr=9FjLWUAryJ1ylTzaev4jYrgV; pl=n; sb=9FjLWW7oPKaIMpeQAuRw_Pbk; locale=en_US')
            end)
  	splash:go(splash.args.url)
  	splash:wait(1)
    return splash:html()
    
    
end"""
class CgtnfranceSpider(scrapy.Spider):
    name = 'cgtnfrance'
    allowed_domains = ['www.facebook.com',
                       'graph.facebook.com']
    # start_urls = ['https://www.facebook.com/login/']
    start_urls = ['https://graph.facebook.com/v2.11/169799706487474/feed?fields=permalink_url%2Cmessage%2Ccreated_time%2Ctype%2Clink&limit=100&access_token=',
        # 'https://graph.facebook.com/v2.11/169799706487474?fields=posts.limit(100)%7Bmessage%2Ccreated_time%2Cid%2Cpermalink_url%2Ctype%7D&access_token='
                  ]
    access_token = 'EAARDVcuRmWMBAOX5emZBl4kYwGDuUZAn1ZBLQKXq2rz8gEPHg5tEdaVZASqd811RUn6MgNNCYDLWKFF3GaOoBR9rqGhVyxHFSAdQ4N4pYPLllrayk47HYCWUAknzyVNzEIZC1rwlAeXqq7OVuts0E0bqZBBjX0DSYjezClOoUOawZDZD'
    cookie = {'act':'1516846265851%2F7','wd':'1181x674',
    'dpr':2,
    'presence':'EDvF3EtimeF1516846151EuserFA21B22221132390A2EstateFDutF1516846151594CEchFDp_5f1B22221132390F0CC',
    'c_user':'100022221132390',
    'fr':'07gv1HLksbxE7qXJL.AWXUDbtk67H-9U6ca1MRbZiuooo.BZy1j0.xE.Fpl.0.0.BaaTXI.AWUzd9As',
    'xs':'39%3Am__JJZZOSY6Sxg%3A2%3A1516764670%3A11335%3A8671',
    'datr':'9FjLWUAryJ1ylTzaev4jYrgV',
    'pl':'n',
    'sb':'9FjLWW7oPKaIMpeQAuRw_Pbk',
    'locale':'en_US'}

    # def start_requests(self):
    #     for url in self.start_urls:
    #         yield SplashRequest(url=url, callback=self.parse,
    #                             args={'wait': 5,
    #                                   'lua_source': PROXY,
    #                                   'js_source': 'document.body',
    #                                   # 'proxy': 'http://127.0.0.1:52031',
    #                                   }, endpoint='render.html')

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url+self.access_token, callback=self.parse,method='GET',cookies=self.cookie)

    def parse(self, response):
        ajson = json.loads(response.text)
        if 'posts' in ajson:
            ajson = ajson['posts']
        alist = ajson['data']
        for item in alist:
            aitem = FacebookPosts()
            aitem['id'] = item['id']
            aitem['created_time'] = item['created_time']
            aitem['permalink_url'] = item['permalink_url']
            aitem['type'] = item['type']
            if 'message' in item:
                aitem['message'] = item['message']
            else:
                aitem['message'] = ''

            yield aitem

        if 'next' in ajson['paging']:
            yield scrapy.Request(url=ajson['paging']['next'], callback=self.parse, method='GET', cookies=self.cookie)
        else:
            print('没有下一页了！')

        # yield SplashRequest(url='https://www.facebook.com/CGTNFrancais/posts/1246231088844325', callback=self.contentParse,
        #                             args={'wait': 5,
        #                                   'lua_source': PROXY,
        #                                   'js_source': 'document.body',
        #                                   # "cookies": self.cookie,
        #                                   }, endpoint='execute')
        pass

    def contentParse(self, response):
        print(response.text)
        pass
