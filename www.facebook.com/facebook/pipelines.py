# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
pymysql.install_as_MySQLdb()
from datetime import datetime
import time
from scrapy.pipelines.files import FilesPipeline
import scrapy
from scrapy.exceptions import DropItem
from facebook.items import FacebookPosts_autor, FacebookPosts_comments
from facebook.items import FacebookPosts_detail, FacebookPosts_file_csv

class MyFilesPipeline(FilesPipeline):
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
    body = '__user=100022221132390&__a=1&__dyn=5V4cjLx2ByK5A9UkKHqAyqomzEmoN7KEyGze8UWC-CGxyEvCU_zoaqhEnUzhUKFGV8iWzoOax2q9wwz8KEjACnyogyEnGi4Fp8CUuF3EK4F8qDho-4EWczo9VoGjx3VVXUW49KcDmiczQq2mEtDxe48B28yaxmi4o9E9omypFVLCypHwxxZomDxnxibyEoGm4UlGiqdy8lxOHCyFEiy9-q26WLBx6m4F5zXBBmF9UZ6pK9J6zpEN2oZ1-ibK6Ux1leqdwxy899Uy9K8Bx7GibwPypuex2cyWVK4F9pF-axvx-8h6cCo8Ulxa9hbx66Ww&__req=20&__be=1&__pc=PHASED:DEFAULT&__rev=3606443&fb_dtsg=AQF6WkPSjz1w:AQFlpxt2STLB&jazoest=26581705487107808310612249119586581701081121201165083847666&__spin_r=3606443&__spin_b=trunk&__spin_t=1517298715'

    def get_media_requests(self, item, info):
        for file_url in item["file_urls"]:
            yield scrapy.Request(file_url,cookies=self.cookie,body=self.body)

    def item_completed(self, results, item, info):
        file_paths = [x["path"] for ok, x in results if ok]
        print(file_paths)
        if not file_paths:
            raise DropItem("Item contains no images")
        return item


class FacebookPipeline(object):
    '''
         异步机制将数据写入到mysql数据库中
         '''

    # 创建初始化函数，当通过此类创建对象时首先被调用的方法
    def __init__(self):
        config = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': '%jGvlz-0<aaTA',
            'db': 'facebook',
            'charset': 'utf8mb4',
            'cursorclass': pymysql.cursors.DictCursor,
        }
        # Connect to the database
        connection = pymysql.connect(**config)
        self.connection = connection

    def process_item(self, item, spider):

        if spider.name == 'facebook_post_mainpage_dairly':
            if isinstance(item, FacebookPosts_detail):
                with self.connection.cursor() as cursor:

                    print(item['created_time'])
                    atime = datetime.strptime(item['created_time'], "%m/%d/%Y %H:%M:%S %p")
                    amessage = ''
                    if 'message' in item:
                        amessage = self.connection.escape(item['message'])
                    if item['id'] == '169799706487474_909127302554707':
                        print(item['id'])
                    insert_sql = 'insert into post_detail_final( f_id, f_message, f_created_time, f_permalink_url, f_shares_count, f_comments_count, f_reactions_counts , f_likes_count, f_type,f_reached_count,f_show_count, f_interaction_count ,  f_use_count ,  f_interaction_mainpage_count  ,  f_video_time_count, f_video_totaltime_count  ,   f_video_view_count , f_photo_view_count , f_link_view_count , f_author ) VALUES("%s","%s","%s","%s",%d,%d, %d,%d,"%s",%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,"%s")' % (
                    item['id'], amessage, atime, item['permalink_url'], item['shares_count'], item['comments_count'],
                    item['reactions_count'], item['likes_count'], item['type'], item['reached_count'],
                    item['show_count'], item['f_interaction_count'], item['f_use_count'],
                    item['f_interaction_mainpage_count'], item['f_video_time_count'], item['f_video_totaltime_count'],
                    item['f_video_view_count'], item['f_photo_view_count'], item['f_link_view_count'], item['f_author'])

                    cursor.execute(insert_sql)
                    self.connection.commit()
            elif isinstance(item, FacebookPosts_autor):
                with self.connection.cursor() as cursor:
                    insert_sql = 'UPDATE post_detail_final SET f_author="%s" WHERE f_id="%s"' % (
                    item['name'], item['id'])
                    print(insert_sql)
                    cursor.execute(insert_sql)
                    self.connection.commit()
            else:
                with self.connection.cursor() as cursor:
                    print(item['created_time'])
                    atime = datetime.strptime(item['created_time'].replace('+0000', ''), "%Y-%m-%dT%H:%M:%S")
                    amessage = ''
                    if 'message' in item:
                        amessage = self.connection.escape(item['message'])

                    insert_sql = 'insert into post_comments(f_id, f_created_time, f_permalink_url ,  f_from_name, f_comments_count , f_from_id, f_likes_count , f_comments_id, f_message ) VALUES("%s","%s","%s","%s", %d,"%s",%d,"%s","%s")' % (
                        item['id'], atime, item['permalink_url'], item['from_name'], item['comments_count'],
                        item['from_id'], item['likes_count'], item['comments_id'], amessage)

                    cursor.execute(insert_sql)
                    self.connection.commit()
        elif spider.name == 'cgtnfrance_post_comments'  or spider.name == 'facebook_xls_comments':

            with self.connection.cursor() as cursor:
                print(item['created_time'])
                atime = datetime.strptime(item['created_time'].replace('+0000', ''), "%Y-%m-%dT%H:%M:%S")
                amessage = ''
                if 'message' in item:
                    amessage = self.connection.escape(item['message'])

                insert_sql = 'insert into post_comments(f_id, f_created_time, f_permalink_url ,  f_from_name, f_comments_count , f_from_id, f_likes_count , f_comments_id, f_message ) VALUES("%s","%s","%s","%s", %d,"%s",%d,"%s","%s")' % (
                    item['id'], atime, item['permalink_url'],item['from_name'],item['comments_count'],item['from_id'],item['likes_count'],item['comments_id'], amessage)

                cursor.execute(insert_sql)
                self.connection.commit()
        elif spider.name == 'facebook_xls_autor':
            with self.connection.cursor() as cursor:
                insert_sql = 'UPDATE post_detail_final SET f_author="%s" WHERE f_id="%s"' %(item['name'] ,item['id'])
                print(insert_sql)
                cursor.execute(insert_sql)
                self.connection.commit()
        elif spider.name == 'facebook_xls':

            with self.connection.cursor() as cursor:

                print(item['created_time'])
                atime = datetime.strptime(item['created_time'], "%m/%d/%Y %H:%M:%S %p")
                amessage = ''
                if 'message' in item:
                    amessage = self.connection.escape(item['message'])
                if item['id'] == '169799706487474_909127302554707':
                    print(item['id'])
                insert_sql = 'insert into post_detail_final( f_id, f_message, f_created_time, f_permalink_url, f_shares_count, f_comments_count, f_reactions_counts , f_likes_count, f_type,f_reached_count,f_show_count, f_interaction_count ,  f_use_count ,  f_interaction_mainpage_count  ,  f_video_time_count, f_video_totaltime_count  ,   f_video_view_count , f_photo_view_count , f_link_view_count , f_author ) VALUES("%s","%s","%s","%s",%d,%d, %d,%d,"%s",%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,"%s")' % (item['id'],amessage, atime, item['permalink_url'], item['shares_count'],item['comments_count'], item['reactions_count'], item['likes_count'], item['type'], item['reached_count'], item['show_count'],item['f_interaction_count'] ,  item['f_use_count']  ,  item['f_interaction_mainpage_count']   ,  item['f_video_time_count'] , item['f_video_totaltime_count']   ,  item['f_video_view_count']  , item['f_photo_view_count']  ,item['f_link_view_count']  , item['f_author'] )

                cursor.execute(insert_sql)
                self.connection.commit()
        elif spider.name == 'facebook_xls_update':

            with self.connection.cursor() as cursor:
                print(item['created_time'])
                atime = datetime.strptime(item['created_time'], "%m/%d/%Y %H:%M:%S %p")
                amessage = ''
                if 'message' in item:
                    amessage = self.connection.escape(item['message'])
                insert_sql = ("UPDATE post_detail SET f_shares_count= %d, f_comments_count=%d, f_reactions_counts=%d, f_likes_count=%d , f_reached_count=%d,f_show_count=%d,f_user_count = %d WHERE f_id=%s" , item['shares_count'],
                    item['comments_count'],
                    item['reactions_count'],
                    item['likes_count'] ,item['reached_count'],
                        item['show_count'],item['user_count'],item['id'])
                cursor.execute(insert_sql)
                self.connection.commit()
        elif spider.name == 'cgtnfrance':
            with self.connection.cursor() as cursor:
                print(item['created_time'])
                atime = datetime.strptime(item['created_time'].replace('+0000', ''), "%Y-%m-%dT%H:%M:%S")
                amessage = ''
                if 'message' in item:
                    amessage = self.connection.escape(item['message'])

                insert_sql = 'insert into CGTNFrancais_post_list(f_id,f_created_time,f_permalink_url,f_message,f_type) VALUES("%s","%s","%s","%s","%s")' % (
                    item['id'], atime, item['permalink_url'], amessage, item['type'])

                cursor.execute(insert_sql)
                self.connection.commit()
