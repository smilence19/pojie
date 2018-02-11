# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FacebookItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class FacebookPosts(scrapy.Item):
    # task name from Redis
    id = scrapy.Field()
    created_time = scrapy.Field()
    permalink_url = scrapy.Field()
    message = scrapy.Field()
    type = scrapy.Field()

class FacebookPosts_comments(scrapy.Item):
    # task name from Redis
    id = scrapy.Field()
    comments_id = scrapy.Field()
    parent_id = scrapy.Field()
    created_time = scrapy.Field()
    permalink_url = scrapy.Field()
    message = scrapy.Field()
    likes_count = scrapy.Field()
    comments_count = scrapy.Field()
    from_name = scrapy.Field()
    from_id = scrapy.Field()

class FacebookPosts_detail(scrapy.Item):
    # task name from Redis
    id = scrapy.Field()
    created_time = scrapy.Field()
    permalink_url = scrapy.Field()
    message = scrapy.Field()
    type = scrapy.Field()
    reached_count = scrapy.Field()
    show_count = scrapy.Field()
    shares_count = scrapy.Field()
    likes_count = scrapy.Field()
    comments_count = scrapy.Field()
    reactions_count = scrapy.Field()
    user_count = scrapy.Field()

    f_interaction_count = scrapy.Field()

    f_use_count = scrapy.Field()

    f_interaction_mainpage_count = scrapy.Field()

    f_video_time_count = scrapy.Field()

    f_video_totaltime_count = scrapy.Field()

    f_video_view_count = scrapy.Field()

    f_photo_view_count = scrapy.Field()

    f_link_view_count = scrapy.Field()

    f_author = scrapy.Field()



class FacebookPosts_file_csv(scrapy.Item):
    # task name from Redis
    name = scrapy.Field()
    file_urls = scrapy.Field()

class FacebookPosts_autor(scrapy.Item):
    # task name from Redis
    name = scrapy.Field()
    id = scrapy.Field()
