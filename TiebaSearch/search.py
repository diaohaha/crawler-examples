#! /usr/bin/env python
#-*- coding: utf-8 -*-

import xapian
import jieba

def search():
	database=xapian.Database('indexes/')
	enquire=xapian.Enquire(database)
	running=1
	while int(running):
		str=raw_input("input the key words:")
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
		print "%i results found" % matches.get_matches_estimated()
		for match in matches:
			a=match.document.get_data()
			d=eval(a)
			print "贴吧:",d["title"]
			print "作者:",d["reply"]["name"]
			print "回复:",d["reply"]["content"]
			print "时间:",d["reply"]["time"]
		running=raw_input("again?(1(yse)/0(no) :")
	print "thank you for using!"	

if __name__ == "__main__":
	search()			
