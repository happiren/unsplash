#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @author happiren

from mysql_manager import MysqlManager

import requests;

#是否开启代理
proxies = {
    "http": "socks5://localhost:1081",
    'https': 'socks5://localhost:1081'
}

mysql = MysqlManager()
headers = {
           'Connection': 'keep-alive',
           'Pragma': 'no-cache',
           'Cache-Control': 'no-cache',
           'Accept': 'application/json, text/javascript, */*; q=0.01',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
           'Accept-Encoding': 'gzip, deflate, br',
           'Accept-Language': 'zh,zh-TW;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6'
           }

class Unsplash:
    def __init__(self):
        self.connection = None

    def get_wallpaper_data(self, page):
        url = "https://unsplash.com/napi/topics/wallpapers/photos?per_page=10&page="+str(page);
        resp = requests.get(url, headers=headers, verify=False); #proxies = proxies
        if (resp.status_code == 200):
            data = {};
            data["type"] = 1
            data["page"] = page
            data["url"] = url
            data["content"] = resp.text
            mysql.insert_wallpaper_data(data)
            return resp.text
        return None;
        print(resp);


