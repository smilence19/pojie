#! /bin/sh
export PATH=$PATH:/usr/local/bin

#进入.py脚本所在目录
cd /www.facebook.com

sudo -s

#执行.py中定义的项目example，并指定日志文件，其中nohup....&表示可以在后台执行，不会因为关闭终端而导致程序执行中断。
nohup sudo scrapy crawl facebook_post_mainpage_dairly >> facebook_post_mainpage_dairly.log 2>&1 &

