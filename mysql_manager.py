#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @author happiren
# @blog  www.happiren.com
import datetime

import pymysql
import time;
from dbutils.pooled_db import PooledDB
import json




class MysqlManager:

    def __init__(self):
        self.connection = None
        self.pool = None
        # 单连接使用
        # self.connection = pymysql.connect(host='localhost',
        #                                   port=3306,
        #                                   user='root',
        #                                   password='123456',
        #                                   database='stock_data',
        #                                   charset='utf8')
        # 使用连接池的方式
        self.pool = PooledDB(pymysql, 5, host='localhost', user='root', passwd='123456', db='wallpaper', port=3306,
                             setsession=[
                                 'SET AUTOCOMMIT = 1'])  # 5为连接池里的最少连接数，setsession=['SET AUTOCOMMIT = 1']是用来设置线程池是否打开自动更新的配置，0为False，1为True
        # self.pool = PooledDB(pymysql, 5, host='test.poooli.cn', user='zhou', passwd='qpzm@7913A', db='xiaohaokj_test_db', port=3306,
        #                      setsession=[
        #                          'SET AUTOCOMMIT = 1'])  # 5为连接池里的最少连接数，setsession=['SET AUTOCOMMIT = 1']是用来设置线程池是否打开自动更新的配置，0为False，1为True
        conn = self.pool.connection()  # 以后每次需要数据库连接就是用connection（）函数获取连接就好了
        self.connection = conn
        print("MysqlManager init")

    '''
    检测数据库中是否有对应的图片
    true:存在 false:不存在
    '''
    def check_wallpaper_pic(self, pic_id):
        sql_str = ("SELECT * "
                   + " FROM usplash_pic"
                   + " WHERE pic_id ='%s'" % (pic_id))
        con = self.pool.connection()
        cur = con.cursor(pymysql.cursors.DictCursor)
        cur.execute(sql_str)
        rows = cur.fetchall()
        if len(rows) >= 1:
            return True
        else:
            return False

    '''
        从数据库中获取所有的壁纸数据
        true:存在 false:不存在
    '''
    def get_wallpapers(self, type):
        sql_str = ("SELECT * "
                   + " FROM usplash_wallpapers"
                   + " WHERE type ='%s'" % (type))
        con = self.pool.connection()
        cur = con.cursor(pymysql.cursors.DictCursor)
        cur.execute(sql_str)
        rows = cur.fetchall()
        if len(rows) >= 1:
            return rows
        else:
            return False

    '''
        根据状态获取一张图片
        true:存在 false:不存在
    '''
    def get_usplash_pic(self, status):
        sql_str = ("SELECT * "
                   + " FROM usplash_pic"
                   + " WHERE status = %s LIMIT 1" % (status))
        con = self.pool.connection()
        cur = con.cursor(pymysql.cursors.DictCursor)
        cur.execute(sql_str)
        rows = cur.fetchall()
        if len(rows) >= 1:
            return rows[0]
        else:
            return False

    '''
        更新图片的状态，用来标记图片下载状态
        true:存在 false:不存在
    '''
    def update_usplash_pic_status(self, pic_id, status):
        con = self.pool.connection()
        cur = con.cursor(pymysql.cursors.DictCursor)
        cur.execute("UPDATE  usplash_pic SET status = %s"
                   + " WHERE pic_id = %s LIMIT 1" ,(status, pic_id))
        rows = cur.fetchall()
        if len(rows) >= 1:
            return rows
        else:
            return False


    '''
        插入壁纸数据
    '''
    def insert_wallpaper_data(self, data):
        # cur = self.connection.cursor()
        con = self.pool.connection()
        cur = con.cursor(pymysql.cursors.DictCursor)
        cur.execute("INSERT INTO usplash_wallpapers(`type`, `page`, `url`,`content`,  `created_at`, `updated_at`) VALUES( %s, %s, %s, %s,%s, %s)",
                    (data["type"], data["page"], data["url"], data["content"],  time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()) , time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()))
                    )
        con.commit()

    '''
    插入壁纸图片
    '''
    def insert_wallpaper_pic(self, data):
        # cur = self.connection.cursor()
        con = self.pool.connection()
        cur = con.cursor(pymysql.cursors.DictCursor)
        data["promoted_at"] = self.defaultconverter(data["promoted_at"])
        data["created_at"] = self.defaultconverter(data["created_at"])
        data["updated_at"] = self.defaultconverter(data["updated_at"])
        cur.execute(
            "INSERT INTO usplash_pic(`pic_id`, `url`, `width`,`height`, `color`,`description`,`alt_description`,`status`,`content`,`promoted_at`, `created_at`, `updated_at`) VALUES( %s, %s, %s,%s,%s, %s, %s, %s,%s, %s, %s, %s)",
            (data["id"], data["urls"]["raw"], data["width"], data["height"],data["color"],data["description"],data["alt_description"], 0 ,json.dumps(data), self.defaultconverter(data["promoted_at"]),
             time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
            )
        con.commit()


    '''
    时间数据转，避免json转换失败
    '''
    def defaultconverter(self, o):
      if isinstance(o, datetime.datetime):
          return o.strftime('Y-m-d H:i:s')



