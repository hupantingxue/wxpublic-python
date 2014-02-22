# -*- coding: utf-8 -*-
import os
import web
import time
import conf
from bs4 import BeautifulSoup
import logging, logging.handlers

urls = ('/', 'index')
loggers = {}

db = web.database(dbn='mysql', user=conf.DB_USER, pw=conf.DB_PWD, db=conf.DB_NAME)

class index:
    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)
        self.wxlogger = self.myLogger('weixin')

    def myLogger(self, name):
        global loggers

        if loggers.get(name):
            return loggers.get(name)
        else:
            logger = logging.getLogger(name)
            logger.setLevel(logging.DEBUG)
            handler = logging.FileHandler(filename='wxrun.log', mode='a')
            formatter = logging.Formatter('[%(name)s:%(lineno)s] - %(asctime)s - %(levelname)s: %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            loggers.update(dict(name=logger))
            return logger

    def GET(self):
        data = web.input()
        signature = data.signature
        timestamp = data.timestamp
        nonce = data.nonce
        echostr = data.echostr
        token = conf.TOKEN
        list = [token, timestamp,nonce]
        list.sort()
        sha1=hashlib.sha1()
        map(sha1.update, list)
        hashcode=sha1.hexdigest()
        if hashcode == signature:
            return echostr

    def POST(self):
        try:
            poststr = web.data()
            soup = BeautifulSoup(poststr, "xml")
            fromuser = soup.FromUserName.text
            touser = soup.ToUserName.text
            frommsgtype = soup.MsgType.text
            curtime = int(time.time())
            echostr = keyword
            #query table 'wx_test' info
            infos = db.select('wx_test', where='title like %$mon%', order='id', vars=locals())
        except Exception as e:
            echostr = "parse fail", e
            self.wxlogger.error("parse fail %s" % (e))
        self.wxlogger.info("poststr[%s]" % (poststr))

        if "text" == frommsgtype:
            keyword = soup.Content.text.strip()
            echostr = keyword
            return self.render.reply_text(fromuser, touser, curtime, u'''我现在还在开发中，还没有什么功能，您刚才说的是：''' + keyword)
        elif "event" == frommsgtype:
            fromevent = soup.Event.text
            return self.render.reply_text(fromuser, touser, curtime, u'''您好，欢迎关注!''')
        else:
            return self.render.reply_text(fromuser, touser, curtime, u'''您好，未知消息。。。''')

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
