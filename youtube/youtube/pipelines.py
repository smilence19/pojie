# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
pymysql.install_as_MySQLdb()
import datetime
from .items import WeiboItem,YoutubeContentItem,WeiboContentItem

class YoutubePipeline(object):
    '''
            异步机制将数据写入到mysql数据库中
            '''

    # 创建初始化函数，当通过此类创建对象时首先被调用的方法
    def __init__(self):
        config = {
            'host': '10.131.54.68',
            'port': 3306,
            'user': 'root',
            'password': 'Ftrwe76!d&*sdjk',
            'db': 'post_db',
            'charset': 'utf8mb4',
            'cursorclass': pymysql.cursors.DictCursor,
        }
        # Connect to the database
        connection = pymysql.connect(**config)
        self.connection = connection

    def process_item(self, item, spider):
        if spider.name == 'weibo_list' or spider.name == 'weibo_daily':
            if isinstance(item, WeiboItem):
                with self.connection.cursor() as cursor:

                    print(item['post_create_time'])
                    atime = datetime.datetime.strptime(item['post_create_time'], "%Y-%m-%d %H:%M")
                    amessage = ''
                    if 'post_message' in item:
                        amessage = self.connection.escape(item['post_message'])
                    play_cout = 0
                    if '万' in str(item['post_play_times']):
                        count_str = item['post_play_times']
                        play_cout = int(float(count_str.replace("万",''))*10000)
                    else:
                        play_cout = int(item['post_play_times'])
                    insert_sql = 'insert into t_weibo(id,postContent,deplyDate,postUrl,postShareCount,postPlCount,postYdCount,postDzCount,vedioPlayCount,vedioLen) VALUES("%s","%s","%s","%s",%d,%d,%d,%d,%d,"%s") on duplicate key update deplyDate=values(deplyDate),postUrl=values(postUrl),postShareCount=values(postShareCount),postPlCount=values(postPlCount),postYdCount=values(postYdCount),postDzCount=values(postDzCount),vedioPlayCount=values(vedioPlayCount),vedioLen=values(vedioLen)' % (item['post_id'],amessage,atime,item['post_url'],int(item['post_shares_times']),int(item['post_comments_times']),int(item['post_watch_times']),int(item['post_likes_times']),play_cout,item['post_video_duration'])
                    print(insert_sql)
                    cursor.execute(insert_sql)
                    self.connection.commit()
            elif isinstance(item, WeiboContentItem):
                with self.connection.cursor() as cursor:
                    if 'post_message' in item:
                        amessage = self.connection.escape(item['post_message'])
                    insert_sql = 'insert into t_weibo(id,postContent) VALUES("%s","%s") on duplicate key update postContent=values(postContent)' % (
                    item['post_id'], amessage)
                    print(insert_sql)
                    cursor.execute(insert_sql)
                    self.connection.commit()
        elif spider.name == 'youtube_videos':
            if isinstance(item, YoutubeContentItem):
                with self.connection.cursor() as cursor:
                    amessage = ''
                    if 'post_video_msg' in item:
                        amessage = self.connection.escape(item['post_video_msg'])

                    insert_sql = 'insert into t_youtube(id,postContent) VALUES("%s","%s") on duplicate key update postContent=values(postContent)' % (
                        item['post_id'], amessage)
                    cursor.execute(insert_sql)
                    self.connection.commit()

            else:
                with self.connection.cursor() as cursor:

                    print(item['post_create_time'])
                    atime = datetime.datetime.strptime(item['post_create_time'], "%Y-%m-%d %H:%M")
                    amessage = ''
                    if 'post_video_title' in item:
                        amessage = self.connection.escape(item['post_video_title'])

                    insert_sql = 'insert into t_youtube(id,postUrl,postTitle,deplyDate,postYdCount,postPlCount,postDzCount,postLikeCount,videolen) VALUES("%s","%s","%s","%s",%d,%d,%d,%d,"%s") on duplicate key update postYdCount=values(postYdCount),postPlCount=values(postPlCount),postDzCount=values(postDzCount),postLikeCount=values(postLikeCount)' % (
                        item['post_id'], item['post_video_url'], amessage, atime, int(item['post_watch_times']),
                        int(item['post_comment_times']),
                        int(item['post_like_times']),
                        int(item['post_dislike_times']),
                        item['post_video_duration'])
                    cursor.execute(insert_sql)
                    self.connection.commit()


        elif spider.name == 'twitter_parse_xls' or spider.name == 'twitter_cvs_daily':
            with self.connection.cursor() as cursor:

                print(item['post_create_time'])
                atime = datetime.datetime.strptime(item['post_create_time'].replace(" +0000",''), "%Y-%m-%d %H:%M")
                atime = atime + datetime.timedelta(hours=8)

                amessage = ''
                if 'post_message' in item:
                    amessage = self.connection.escape(item['post_message'])

                insert_sql='insert into twitter_post_list(id,postContent,postUrl,deplyDate,postZsCount,postHdCount,postHdRate,postZfCount,postPlCount,postDzCount,urlDjCount,videoGkCount,videoCyCount,payZsCount,payHdCount,payHdRate,payZfCount,payPlCount,payDzCount,payUrlCount,payVedioGkCount,payVedioCyCount) VALUES("%s","%s","%s","%s",%f,%f,%s,%f,%f,%f,%f,%f,%f,%f,%f,"%s",%f,%f,%f,%f,%f,%f) on duplicate key update deplyDate=values(deplyDate),postContent=values(postContent),postZsCount=values(postZsCount),postHdCount=values(postHdCount),postHdRate=values(postHdRate),postZfCount=values(postZfCount),postPlCount=values(postPlCount),postDzCount=values(postDzCount),urlDjCount=values(urlDjCount),videoGkCount=values(videoGkCount),videoCyCount=values(videoCyCount),payZsCount=values(payZsCount),payHdCount=values(payHdCount),payHdRate=values(payHdRate),payZfCount=values(payZfCount),payPlCount=values(payPlCount),payDzCount=values(payDzCount),payUrlCount=values(payUrlCount),payVedioGkCount=values(payVedioGkCount),payVedioCyCount=values(payVedioCyCount)' % (
                item['post_id'],amessage, item['post_url'], atime,
                float(item['post_show_times']), float(item['post_hudong_times']), item['post_hudong_rate'], float(item['post_shares_times']),
                float(item['post_comments_times']), float(item['post_like_times']), float(item['post_url_click_count']),
                float(item['post_video_watch_times']), float(item['post_video_hudong_times']), float(item['post_show_times_fee']),
                float(item['post_hudong_times_fee']), item['post_hudong_rate_fee'], float(item['post_shares_times_fee']),
                float(item['post_comments_times_fee']), float(item['post_like_times_fee']), float(item['post_url_click_count_fee']),
                float(item['post_video_watch_times_fee']), float(item['post_video_hudong_times_fee']))
                print(insert_sql)
                cursor.execute(insert_sql)
                self.connection.commit()


        return item
