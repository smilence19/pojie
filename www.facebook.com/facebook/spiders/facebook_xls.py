# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest, SplashFormRequest
from scrapy import Selector
from scrapy.http.request import Request
from scrapy.http.request.form import FormRequest
from scrapy.spiders.init import InitSpider
from scrapy.exceptions import CloseSpider
from facebook.items import FacebookPosts
from facebook.items import FacebookPosts_detail
import re
import json
import datetime
import sys
import xlrd
import csv
import os



class FacebookxlsSpider(InitSpider):
    name = 'facebook_xls'
    allowed_domains = ['www.facebook.com',
                       'graph.facebook.com']
    login_url = "https://www.baidu.com/"
    start_urls = [ "https://www.baidu.com/"]

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
                if len(i)>34 and i[34]:
                    item['shares_count'] = int(i[34])
                else:
                    item['shares_count'] = 0
                if len(i)>35 and i[35]:
                    item['likes_count'] = int(i[35])
                else:
                    item['likes_count'] = 0
                if len(i)>36 and i[36]:
                    item['comments_count'] = int(i[36])
                else:
                    item['comments_count'] = 0
                if len(i)>40 and i[40]:
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
                    item['f_video_time_count']  = int(i[32])
                else:
                    item['f_video_time_count'] = 0

                if len(i) > 33 and i[33]:
                    item['f_video_totaltime_count']  = int(i[33])
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
                yield item





