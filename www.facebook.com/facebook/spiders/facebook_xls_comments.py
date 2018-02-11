# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest, SplashFormRequest
from scrapy import Selector
from scrapy.http.request import Request
from scrapy.http.request.form import FormRequest
from scrapy.spiders.init import InitSpider
from scrapy.exceptions import CloseSpider
from facebook.items import FacebookPosts_comments
from facebook.items import FacebookPosts_detail
import re
import json
import datetime
import sys
import xlrd
import csv
import os



class FacebookxlsSpider(InitSpider):
    name = 'facebook_xls_comments'
    allowed_domains = ['www.facebook.com',
                       'graph.facebook.com']
    login_url = "https://www.baidu.com/"
    start_urls = [ "https://www.google.com/"]

    access_token = 'EAARDVcuRmWMBAOX5emZBl4kYwGDuUZAn1ZBLQKXq2rz8gEPHg5tEdaVZASqd811RUn6MgNNCYDLWKFF3GaOoBR9rqGhVyxHFSAdQ4N4pYPLllrayk47HYCWUAknzyVNzEIZC1rwlAeXqq7OVuts0E0bqZBBjX0DSYjezClOoUOawZDZD'
    cookie = {'act': '1516846265851%2F7', 'wd': '1181x674',
              'dpr': 2,
              'presence': 'EDvF3EtimeF1516846151EuserFA21B22221132390A2EstateFDutF1516846151594CEchFDp_5f1B22221132390F0CC',
              'c_user': '100022221132390',
              'fr': '07gv1HLksbxE7qXJL.AWXUDbtk67H-9U6ca1MRbZiuooo.BZy1j0.xE.Fpl.0.0.BaaTXI.AWUzd9As',
              'xs': '39%3Am__JJZZOSY6Sxg%3A2%3A1516764670%3A11335%3A8671',
              'datr': '9FjLWUAryJ1ylTzaev4jYrgV',
              'pl': 'n',
              'sb': '9FjLWW7oPKaIMpeQAuRw_Pbk',
              'locale': 'en_US'}

    def parse(self, response):

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
        filename_list = []
        for root, dirs, files in os.walk('/Users/huangqingjun/git/www.facebook.com/full'):
            print(files)
            filename_list = files
        for file_name in filename_list:
            print(file_name)
            if file_name == '0e341de0f4f2afce9370910fdc94d4bde80eefea':
                print(file_name)
            if '.DS_Store' in file_name:
                continue
            csv_file = csv.reader(open('/Users/huangqingjun/git/www.facebook.com/full/'+ file_name, 'r'))
            n = 0
            for i in csv_file:
                n = n + 1
                if n <= 2:
                    continue
                print(i)
                comments_id = i[0]
                yield scrapy.Request(
                    url='https://graph.facebook.com/v2.11/' + comments_id + '?fields=comments.limit(100)%7Bid%2Cmessage%2Clike_count%2Ccreated_time%2Cpermalink_url%2Ccomment_count%2Cfrom%7D%2Cid&access_token=' + self.access_token,
                    callback=self.comments_parse, method='GET', cookies=self.cookie)

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





