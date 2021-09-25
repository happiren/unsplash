#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @author happiren
import urllib
import json
import _thread

from mysql_manager import MysqlManager
from unsplash import Unsplash
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import requests;
mysql = MysqlManager()
unsplash_cli = Unsplash()





def scrapWallPapers(pages):
    # with open("resp_demo.txt", "r") as f:
    #     str_resp = json.load(f)
    for i in range(0, pages):
        resp = unsplash_cli.get_wallpaper_data(i)
        if not resp:
            print("error page:"+str(i))
            exit(0)
        resp_json = json.loads(resp)
        # resp_json = str_resp;
        print("wallpaper data finished total pages :"+str(i))


def convertWallPaperPics():
    rows = mysql.get_wallpapers(1);
    count = 0;
    for row in rows:
        count = count + 1;
        print("row:"+str(count))
        pics = json.loads(row["content"]);
        for pic in pics:
            if (mysql.check_wallpaper_pic(pic["id"])):
                print("pic exit:" + pic["id"])
            else:
                mysql.insert_wallpaper_pic(pic)
    print("wallpaper convert finished! ")

def savePicThread(name):
    while True:
        pic = mysql.get_usplash_pic(1)
        if pic:
            mysql.update_usplash_pic_status(pic["pic_id"], 1);
            resp = requests.get(pic['url']);
            file_name = "H:/图片/usplash/"+pic["pic_id"] + ".jpg";
            with open(file_name, "wb") as f:
                f.write(resp.content)  # 保存文件
            mysql.update_usplash_pic_status(pic["pic_id"], 2);
            print(name + ":" + file_name);
        else:
            print(name + ":线程退出")
            return;


def downloadPics(threads):
    print("download pic start!")
    for i in range(1, threads):
        _thread.start_new_thread(savePicThread, ("Thread-"+str(i), ))


def main():
    scrapWallPapers(1000); #爬取图片数据并保存到数据库
    convertWallPaperPics(); #转换图片数据并为每张图片单独保存一条记录
    downloadPics(50);   #开启多线程下载图片
    #线程资源回收就不处理，直接结束程序

if __name__ == "__main__":
    main()