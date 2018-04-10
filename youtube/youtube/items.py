# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YoutubeItem(scrapy.Item):
    # define the fields for your item here like:
    post_id = scrapy.Field()
    post_video_url = scrapy.Field()
    post_video_title = scrapy.Field()
    post_video_duration = scrapy.Field()
    post_create_time = scrapy.Field()
    post_watch_times = scrapy.Field()
    post_comment_times = scrapy.Field()
    post_like_times = scrapy.Field()
    post_dislike_times = scrapy.Field()
    pass

class YoutubeContentItem(scrapy.Item):
    post_id = scrapy.Field()
    post_video_msg = scrapy.Field()

class WeiboItem(scrapy.Item):
    # define the fields for your item here like:
    post_id = scrapy.Field()
    post_message = scrapy.Field()
    post_url = scrapy.Field()
    post_create_time = scrapy.Field()
    post_watch_times = scrapy.Field()
    post_comments_times = scrapy.Field()
    post_likes_times = scrapy.Field()
    post_shares_times = scrapy.Field()
    post_play_times = scrapy.Field()
    post_video_duration = scrapy.Field()
    pass
class WeiboContentItem(scrapy.Item):
    # define the fields for your item here like:
    post_id = scrapy.Field()
    post_message = scrapy.Field()
    pass

class TwitterItem(scrapy.Item):
    # define the fields for your item here like:
    post_id = scrapy.Field()
    post_message = scrapy.Field()
    post_url = scrapy.Field()
    post_create_time = scrapy.Field()
    #展示量
    post_show_times = scrapy.Field()
    # 互动
    post_hudong_times = scrapy.Field()
    # 互动率
    post_hudong_rate = scrapy.Field()
    #转发
    post_shares_times = scrapy.Field()
    #回复
    post_comments_times = scrapy.Field()
    #赞
    post_like_times = scrapy.Field()

    #url点击数
    post_url_click_count = scrapy.Field()

    #媒体观看量
    post_video_watch_times = scrapy.Field()
    # 媒体参与
    post_video_hudong_times = scrapy.Field()

    # 推广展示量
    post_show_times_fee = scrapy.Field()
    # 推广互动
    post_hudong_times_fee = scrapy.Field()
    # 推广互动率
    post_hudong_rate_fee = scrapy.Field()
    # 推广转发
    post_shares_times_fee = scrapy.Field()
    # 推广回复
    post_comments_times_fee = scrapy.Field()
    # 推广赞
    post_like_times_fee = scrapy.Field()

    # 推广url点击数
    post_url_click_count_fee = scrapy.Field()
    #"推广的 媒体观看量",
    post_video_watch_times_fee = scrapy.Field()
    #"推广的 媒体参与"
    post_video_hudong_times_fee = scrapy.Field()
    pass