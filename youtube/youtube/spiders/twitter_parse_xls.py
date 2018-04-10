# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders.init import InitSpider
from youtube.items import TwitterItem


import csv
import os



class FacebookxlsSpider(InitSpider):
    name = 'twitter_parse_xls'
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
        for root, dirs, files in os.walk('/Users/huangqingjun/git/youtube/csv'):
            print(files)
            filename_list = files
        for file_name in filename_list:
            print(file_name)
            if '.DS_Store' in file_name:
                continue
            csv_file = csv.reader(open('/Users/huangqingjun/git/youtube/csv/'+ file_name, 'r'))
            n = 0
            for i in csv_file:
                if n == 0:
                    n = 1
                    continue



                item = TwitterItem()
                item['post_id']= i[0]
                item['post_message']= i[2]
                item['post_url']= i[1]
                item['post_create_time'] = i[3]
                item['post_show_times'] = i[4]
                item['post_hudong_times'] = i[5]
                item['post_hudong_rate'] = i[6]
                item['post_shares_times'] = i[7]
                item['post_comments_times'] = i[8]
                item['post_like_times'] = i[9]
                item['post_url_click_count'] = i[11]
                item['post_video_watch_times'] = i[20]
                item['post_video_hudong_times'] = i[21]
                if i[22] == '-':
                    item['post_show_times_fee'] = 0
                else:
                    item['post_show_times_fee'] = i[22]
                if i[23] == '-':
                    item['post_hudong_times_fee'] = 0
                else:
                    item['post_hudong_times_fee'] = i[23]

                item['post_hudong_rate_fee'] = i[24]

                if i[25] == '-':
                    item['post_shares_times_fee'] =0
                else:
                    item['post_shares_times_fee'] = i[25]

                if i[26] == '-':
                    item['post_comments_times_fee'] =0
                else:
                    item['post_comments_times_fee'] = i[26]

                if i[27] == '-':
                    item['post_like_times_fee'] =0
                else:
                    item['post_like_times_fee'] = i[27]

                if i[29] == '-':
                    item['post_url_click_count_fee'] = 0
                else:
                    item['post_url_click_count_fee'] = i[29]

                if i[38] == '-':
                    item['post_video_watch_times_fee'] = 0
                else:
                    item['post_video_watch_times_fee'] = i[38]

                if i[39] == '-':
                    item['post_video_hudong_times_fee'] = 0
                else:
                    item['post_video_hudong_times_fee'] = i[39]
                yield item





