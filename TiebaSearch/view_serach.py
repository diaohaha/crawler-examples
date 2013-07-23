#! /usr/bin/env python
#-*- coding: utf-8 -*-

import tornado.ioloop
import tornado.web
import xapian
import jieba
import os
from tornado import template


def search(str):
	database=xapian.Database('indexes/')
	enquire=xapian.Enquire(database)
	terms=[]
	a=jieba.cut_for_search(str)
	for b in a:
		terms.append(b.encode("utf-8"))
	qp=xapian.QueryParser()#建立查询分析
	qp.set_database(database)
	qp.set_default_op(xapian.Query.OP_AND)#设置查询策略 
	#query = qp.parse_query(terms)
	query = xapian.Query(xapian.Query.OP_OR,terms)#查询函数，搞不懂
	enquire.set_query(query)
	matches = enquire.get_mset(0, 10)
	return matches
	
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('<html><body><form action="/" method="post">'
                   '<h4>峨眉山贴吧查询：</h4>'
                   '<input type="text" name="message">'
                   '<input type="submit" value="Search">'
                   '</form></body></html>')

    def post(self):
		#self.set_header("Content-Type", "text/plain")
		str=self.get_argument("message")
		matches=search(str)
		loader =template.Loader(os.path.dirname(__file__))
		t=loader.load("result.html")
		i=0
		results=[]
		num=matches.get_matches_estimated()
		for match in matches:
			result=match.document.get_data()
			dresult=eval(result)
			results.append(dresult)
		htmlsrc=t.generate(results=results,num=num)
		self.write(htmlsrc)	

application = tornado.web.Application([
    (r"/", MainHandler),
])

if __name__ == "__main__":
    application.listen(8080)
    tornado.ioloop.IOLoop.instance().start()
