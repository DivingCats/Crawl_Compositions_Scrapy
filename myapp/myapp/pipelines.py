# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql

class MyappPipeline(object):

    def __init__(self):
        self.conn = pymysql.connect(host="localhost", user="root", passwd="learnmysql", db="article")
        print("build mysql connetion successful!")

    def process_item(self, item, spider):
        title = item["articletitle"][0]
        detail=''
        for i in range(0, len(item["articledetail"])):
            detail += item["articledetail"][i]
        sql = "INSERT INTO winter(article_title, article_detail) VALUES ('%s', '%s')" % (title, detail)
        try:
            self.conn.query(sql)
            self.conn.commit()
            print("insert article title is " + title)
        except:
            print("insert fault")

        return item

    def close_spider(self, spider):

        self.conn.close()
        print("close mysql connection!")
