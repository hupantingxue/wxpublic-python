# -*- coding: utf-8 -*-
import os
import web
import time
from bs4 import BeautifulSoup
import logging, logging.handlers

urls = ('/', 'index')
loggers = {}

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
            logger=logging.getLogger(name)
            logger.setLevel(logging.DEBUG)
            handler=logging.FileHandler(filename='wxrun.log', mode='a')
            formatter = logging.Formatter('[%(name)s:%(lineno)s] - %(asctime)s - %(levelname)s: %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            loggers.update(dict(name=logger))
            return logger

    def POST(self):
        try:
            poststr = web.data()
            soup = BeautifulSoup(poststr, "xml")
            fromuser = soup.FromUserName.text
            touser = soup.ToUserName.text
            frommsgtype = soup.MsgType.text
            keyword = soup.Content.text.strip()
            curtime = int(time.time())
            echostr = keyword
        except Exception as e:
            echostr = "parse fail", e
            self.wxlogger.error("parse fail %s" % (e))
        self.wxlogger.info("poststr[%s]" % (poststr))
        print poststr
        return self.render.reply_text(fromuser, touser, curtime, u'''我现在还在开发中，还没有什么功能，您刚才说的是：''' + keyword)

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
