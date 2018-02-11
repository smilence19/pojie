# -*- coding: utf-8 -*-
import scrapy
# from scrapy_splash import SplashRequest, SplashFormRequest
# from scrapy import Selector
# from scrapy.http.request import Request
# from scrapy.http.request.form import FormRequest
from scrapy.spiders.init import InitSpider
# from scrapy.exceptions import CloseSpider
from facebook.items import FacebookPosts_autor, FacebookPosts_comments
from facebook.items import FacebookPosts_detail, FacebookPosts_file_csv
import re
import json
import datetime
import time
import sys
import xlrd
import csv
import os
from urllib.parse import urlencode




class FacebookxlsSpider(InitSpider):
    name = 'facebook_post_mainpage_dairly'
    allowed_domains = ['www.facebook.com',
                       'graph.facebook.com']
    start_urls = [
        "https://www.facebook.com/insights/async/export_page_insights/?page_id=169799706487474&platform=www&section=navOverview&data_level=post_level&start_time_text_field=1%2F3%2F2016&end_time_text_field=1%2F30%2F2016&file_format=csv&format_id=639968596200508&ui_start_timestamp=1517298715638&dpr=2",
    # 'https://www.facebook.com/insights/async/report_check/?export_run_id=546204765758478&dpr=2'
    ]
    cookie = {'act': '1517277644633%2F4', 'wd': '1280x326',
              'dpr': 2,
              'presence': 'EDvF3EtimeF1517277609EuserFA21B22221132390A2EstateFDt3F_5b_5dG517277609282CEchFDp_5f1B22221132390F7CC',
              'c_user': '100022221132390',
              'fr': '07gv1HLksbxE7qXJL.AWVxdcndVH1aNzdx_Hu1d0al-j8.BZy1j0.xE.Fpl.0.0.Bab8Zw.AWVRlev-',
              'xs': '39%3Am__JJZZOSY6Sxg%3A2%3A1516764670%3A11335%3A8671',
              'datr': '9FjLWUAryJ1ylTzaev4jYrgV',
              'pl': 'n',
              'sb': '9FjLWW7oPKaIMpeQAuRw_Pbk',
              'locale': 'en_US'}
    header = {
        'Referer': 'https://www.facebook.com/CGTNFrancais/insights/?section=navOverview',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://www.facebook.com',
    'Host': 'www.facebook.com',
    'Accept': '*/*',
    'Connection': 'keep-alive',
    'Accept-Language': 'zh-cn',
    'Accept-Encoding': 'gzip, deflate',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0.3 Safari/604.5.6'
    }
    access_token = 'EAARDVcuRmWMBAOX5emZBl4kYwGDuUZAn1ZBLQKXq2rz8gEPHg5tEdaVZASqd811RUn6MgNNCYDLWKFF3GaOoBR9rqGhVyxHFSAdQ4N4pYPLllrayk47HYCWUAknzyVNzEIZC1rwlAeXqq7OVuts0E0bqZBBjX0DSYjezClOoUOawZDZD'

    body ='__user=100022221132390&__a=1&__dyn=5V4cjLx2ByK5A9UkKHqAyqomzEmoN7KEyGze8UWC-CGxyEvCU_zoaqhEnUzhUKFGV8iWzoOax2q9wwz8KEjACnyogyEnGi4Fp8CUuF3EK4F8qDho-4EWczo9VoGjx3VVXUW49KcDmiczQq2mEtDxe48B28yaxmi4o9E9omypFVLCypHwxxZomDxnxibyEoGm4UlGiqdy8lxOHCyFEiy9-q26WLBx6m4F5zXBBmF9UZ6pK9J6zpEN2oZ1-ibK6Ux1leqdwxy899Uy9K8Bx7GibwPypuex2cyWVK4F9pF-axvx-8h6cCo8Ulxa9hbx66Ww&__req=20&__be=1&__pc=PHASED:DEFAULT&__rev=3606443&fb_dtsg=AQF6WkPSjz1w:AQFlpxt2STLB&jazoest=26581705487107808310612249119586581701081121201165083847666&__spin_r=3606443&__spin_b=trunk&__spin_t=1517298715'
    last_dateTime = datetime.datetime.now()
    timestr = str(int(time.time()))
    def start_requests(self):
        for url in self.start_urls:
            now_time = self.last_dateTime
            yes_time = now_time + datetime.timedelta(days=-30)
            # self.last_dateTime = yes_time
            now_data = now_time.strftime('%m/%d/%Y').replace('/','%2F')
            yes_date = yes_time.strftime('%m/%d/%Y').replace('/','%2F')
            aurl= 'https://www.facebook.com/insights/async/export_page_insights/?page_id=169799706487474&platform=www&section=navOverview&data_level=post_level&start_time_text_field='+yes_date+'&end_time_text_field='+now_data+'&file_format=csv&format_id=639968596200508&ui_start_timestamp='+\
                  str(int(round(time.time() * 1000)))+'&dpr=2'
            body = '__user=100022221132390&__a=1&__dyn=5V4cjLx2ByK5A9UkKHqAyqomzFEZz4uWyaF2-8VpQC-CGgjKEvCUVqyEaqhEnUzhUKFGV8iWzppEG49EC22cyWDyV9BUC48G5WAxamjDKaxeAcUK4F98lDp8-4ER2KdyUrBAAhfypfBVXUW49KcDmiczQq5o-EtBUjByEB94y8G5p8hwCwBxlemqurVe9CJ0wxZomCgWrxjBKaxyFojxmF9kdxCi7aKHyFE-EyvCDgoKHVoghoiAnyrKmlqADza8IHm9IzgSqck-8CgvAG8Kqify4cBFeqdwxy8G6pUy9K8Bz_HGby8Gdx69AmeyV8CJ2aQnByLHKqvyElZaiaBBDp6cCo8Vp8GdJ2kiUhDzAWDLBg&__req=27&__be=1&__pc=PHASED:DEFAULT&__rev=3637446&fb_dtsg=AQGkG_aG4Jkt:AQFZGUeWKEgj&jazoest=265817110771959771527410711658658170907185101877569103106&__spin_r=3637446&__spin_b=trunk&__spin_r= 3637446&__spin_t=' + self.timestr
            yield scrapy.Request(url=aurl, callback=self.parse,method='POST',headers=self.header,cookies=self.cookie,body=body)

    def parse(self, response):

        print('返回结果'+response.text)
        p = re.compile(r'asyncExport(.*?)}')
        matcher1 = re.search(p, response.text)
        result = ''
        if matcher1:
            result = matcher1.group(1)

        aid = ''
        if result:
            aid = result.replace('\"','').replace(',','').replace('[','').replace(']','')
        p1 = re.compile(r'exportFile",(.*?),(.*?),')
        matcher = re.search(p1, response.text)
        if matcher:
            result = matcher.group(2)
            aid = result.replace('\"','').replace(',','').replace('[','').replace(']','')
            link = 'https://www.facebook.com/insights/export_page_insights_file/?export_run_id='+ aid
            item = FacebookPosts_file_csv()
            item['file_urls'] =[link]
            item['name'] = self.last_dateTime.strftime('%Y/%m/%d')
            yield scrapy.Request(link, cookies=self.cookie, body=self.body,callback=self.postParse)

            # now_time = self.last_dateTime
            # yes_time = now_time + datetime.timedelta(days=-10)
            # self.last_dateTime = yes_time
            # now_data = now_time.strftime('%m/%d/%Y').replace('/', '%2F')
            # yes_date = yes_time.strftime('%m/%d/%Y').replace('/', '%2F')
            # aurl = 'https://www.facebook.com/insights/async/export_page_insights/?page_id=169799706487474&platform=www&section=navOverview&data_level=post_level&start_time_text_field=' + yes_date + '&end_time_text_field=' + now_data + '&file_format=csv&format_id=639968596200508&ui_start_timestamp=' + \
            #        str(int(round(time.time() * 1000))) + '&dpr=2'
            # body = '__user=100022221132390&__a=1&__dyn=5V4cjLx2ByK5A9UkKHqAyqomzEmoN7KEyGze8UWC-CGxyEvCU_zoaqhEnUzhUKFGV8iWzoOax2q9wwz8KEjACnyogyEnGi4Fp8CUuF3EK4F8qDho-4EWczo9VoGjx3VVXUW49KcDmiczQq2mEtDxe48B28yaxmi4o9E9omypFVLCypHwxxZomDxnxibyEoGm4UlGiqdy8lxOHCyFEiy9-q26WLBx6m4F5zXBBmF9UZ6pK9J6zpEN2oZ1-ibK6Ux1leqdwxy899Uy9K8Bx7GibwPypuex2cyWVK4F9pF-axvx-8h6cCo8Ulxa9hbx66Ww&__req=20&__be=1&__pc=PHASED:DEFAULT&__rev=3606443&fb_dtsg=AQF6WkPSjz1w:AQFlpxt2STLB&jazoest=26581705487107808310612249119586581701081121201165083847666&__spin_r=3606443&__spin_b=trunk&__spin_t='+str(int(time.time()))
            # yield scrapy.Request(url=aurl, callback=self.parse, method='POST', headers=self.header, cookies=self.cookie,
            #                      body=self.body)

        else:
            body = '__user=100022221132390&__a=1&__dyn=5V4cjLx2ByK5A9UkKHqAyqomzFEZz4uWyaF2-8VpQC-CGgjKEvCUVqyEaqhEnUzhUKFGV8iWzppEG49EC22cyWDyV9BUC48G5WAxamjDKaxeAcUK4F98lDp8-4ER2KdyUrBAAhfypfBVXUW49KcDmiczQq5o-EtBUjByEB94y8G5p8hwCwBxlemqurVe9CJ0wxZomCgWrxjBKaxyFojxmF9kdxCi7aKHyFE-EyvCDgoKHVoghoiAnyrKmlqADza8IHm9IzgSqck-8CgvAG8Kqify4cBFeqdwxy8G6pUy9K8Bz_HGby8Gdx69AmeyV8CJ2aQnByLHKqvyElZaiaBBDp6cCo8Vp8GdJ2kiUhDzAWDLBg&__req=27&__be=1&__pc=PHASED:DEFAULT&__rev=3637446&fb_dtsg=AQGkG_aG4Jkt:AQFZGUeWKEgj&jazoest=265817110771959771527410711658658170907185101877569103106&__spin_r=3637446&__spin_b=trunk&__spin_r= 3637446&__spin_t=' + self.timestr
            yield scrapy.Request(url='https://www.facebook.com/insights/async/report_check/?export_run_id='+aid+'&dpr=2', callback=self.parse, method='POST', headers=self.header, cookies=self.cookie,body=body,dont_filter=True)

        # excelFile = xlrd.open_workbook(r'Post Level.xls')
        # sheet = excelFile.sheet_by_index(0)
        # # 获取第一列的所有值
        # cv = sheet.col_values(1, start_rowx=1, end_rowx=None)
        #
        # #循环打印每一行
        # nrows = sheet.nrows
        # for i in range(nrows):
        #     if i == 0:
        #         continue
        #     print(sheet.row_values(i)[0])

        # csv_file = csv.reader(open('facebookposts.csv','r'))
        # n = 0
        # for i in csv_file:
        #     n = n+1
        #     if n <=2:
        #         continue
        #     print(i)
        #     item = FacebookPosts_detail()
        #     item['id'] = i[0]
        #     item['created_time'] = i[6]
        #     item['permalink_url'] = i[1]
        #     item['message'] = i[2]
        #     item['type'] = i[3]
        #     if i[8]:
        #         item['reached_count'] = int(i[8])
        #     else:
        #         item['reached_count'] = 0
        #     if i[11]:
        #         item['show_count'] = int(i[11])
        #     else:
        #         item['show_count'] = 0
        #     if i[34]:
        #         item['shares_count'] = int(i[34])
        #     else:
        #         item['shares_count'] = 0
        #     if i[35]:
        #         item['likes_count'] = int(i[35])
        #     else:
        #         item['likes_count'] = 0
        #     if i[36]:
        #         item['comments_count'] = int(i[36])
        #     else:
        #         item['comments_count'] = 0
        #     if i[40]:
        #         item['reactions_count'] = int(i[40])
        #     else:
        #         item['reactions_count'] = 0
        #     yield item
    def postParse(self, response):

        fh = open('dairly_csv.csv', 'w')
        fh.write(response.text)
        fh.close()
        csv_file = csv.reader(open('dairly_csv.csv', 'r'))
        n = 0
        for i in csv_file:
            n = n + 1
            if n <= 2:
                continue
            print(i)
            item = FacebookPosts_detail()
            item['id'] = i[0]
            if i[0] == '169799706487474_909127302554707':
                print(i[0])
            item['created_time'] = i[6]
            item['permalink_url'] = i[1]
            item['message'] = i[2]
            item['type'] = i[3]
            if i[8]:
                item['reached_count'] = int(i[8])
            else:
                item['reached_count'] = 0
            if i[11]:
                item['show_count'] = int(i[11])
            else:
                item['show_count'] = 0
            if len(i) > 34 and i[34]:
                item['shares_count'] = int(i[34])
            else:
                item['shares_count'] = 0
            if len(i) > 35 and i[35]:
                item['likes_count'] = int(i[35])
            else:
                item['likes_count'] = 0
            if len(i) > 36 and i[36]:
                item['comments_count'] = int(i[36])
            else:
                item['comments_count'] = 0
            if len(i) > 40 and i[40]:
                item['reactions_count'] = int(i[40])
            else:
                item['reactions_count'] = 0
            if len(i) > 14 and i[14]:
                item['f_interaction_count'] = int(i[14])
            else:
                item['f_interaction_count'] = 0
            if len(i) > 16 and i[16]:
                item['f_use_count'] = int(i[16])
            else:
                item['f_use_count'] = 0

            if len(i) > 23 and i[23]:
                item['f_interaction_mainpage_count'] = int(i[23])
            else:
                item['f_interaction_mainpage_count'] = 0
            if len(i) > 32 and i[32]:
                item['f_video_time_count'] = int(i[32])
            else:
                item['f_video_time_count'] = 0

            if len(i) > 33 and i[33]:
                item['f_video_totaltime_count'] = int(i[33])
            else:
                item['f_video_totaltime_count'] = 0

            if len(i) > 42 and i[42]:
                item['f_video_view_count'] = int(i[42])
            else:
                item['f_video_view_count'] = 0

            if len(i) > 43 and i[43]:
                item['f_photo_view_count'] = int(i[43])
            else:
                item['f_photo_view_count'] = 0

            if len(i) > 41 and i[41]:
                item['f_link_view_count'] = int(i[41])
            else:
                item['f_link_view_count'] = 0
            item['f_author'] = ''

            comments_id = i[0]
            yield scrapy.Request(
                url='https://graph.facebook.com/v2.11/' + comments_id + '?fields=admin_creator&access_token=' + self.access_token,
                callback=self.author_parse, method='GET', cookies=self.cookie)
            yield scrapy.Request(
                url='https://graph.facebook.com/v2.11/' + comments_id + '?fields=comments.limit(100)%7Bid%2Cmessage%2Clike_count%2Ccreated_time%2Cpermalink_url%2Ccomment_count%2Cfrom%7D%2Cid&access_token=' + self.access_token,
                callback=self.comments_parse, method='GET', cookies=self.cookie)
            yield item


    def author_parse(self, response):
        ajson = json.loads(response.text)
        key_id = ajson['id']
        if 'admin_creator' in ajson:
            ajson = ajson['admin_creator']
            name = ajson['name']
            print(name)
            item = FacebookPosts_autor()
            item['name'] =name
            item['id'] = key_id
            yield item

    def comments_parse(self, response):
        ajson = json.loads(response.text)
        key_id = ajson['id']
        if 'comments' in ajson:
            ajson = ajson['comments']
            alist = ajson['data']
            for item in alist:
                aitem = FacebookPosts_comments()
                aid = str(item['id'])
                aitem['id'] = key_id + '_' +aid.split('_')[1]
                aitem['comments_id'] = aid
                aitem['created_time'] = item['created_time']
                aitem['permalink_url'] = item['permalink_url']
                aitem['likes_count'] = item['like_count']
                aitem['comments_count'] = item['comment_count']
                aitem['from_name'] = item['from']['name']
                aitem['from_id'] = item['from']['id']
                if 'message' in item:
                    aitem['message'] = item['message']
                else:
                    aitem['message'] = ''

                yield aitem
            if 'next' in ajson['paging']:
                yield scrapy.Request(url=ajson['paging']['next'], callback=self.comments_parse, method='GET',
                                     cookies=self.cookie)
            else:
                print('没有下一页了！')


