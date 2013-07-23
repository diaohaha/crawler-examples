#!usr/bin/env python
# -*- coding: utf-8 -*-

#filename:make_index
#author:gaoda
#date:2013.6.9
#describe:建立json格式索引

import json
import xapian
import jieba


def make_index():
	dbfile=file("tieba.json")
	dat=dbfile.read()
	datas=dat.split('\n')
	database = xapian.WritableDatabase('indexes/', xapian.DB_CREATE_OR_OPEN)
	#stemmer = xapian.Stem("english")
	for data in datas:
		try:
			ddata=eval(data)
			use_data={}
			use_data["title"]=ddata["title"]
			reply={}
			reply["content"]=ddata["reply"]["content"]
			reply["name"]=ddata["reply"]["name"]
			reply["time"]=ddata["reply"]["time"]
			use_data["reply"]=reply
			doc = xapian.Document()
			doc.set_data(str(use_data))
			use_data=str(ddata["reply"]["name"])+str(ddata["reply"]["time"])+str(ddata["reply"]["content"])+str(ddata["title"])
			for term in jieba.cut_for_search(str(use_data)):
				doc.add_term(term.encode('utf-8'))
			database.add_document(doc)
		except:
			pass	
	database.commit()
	dbfile.close()
	
if __name__ == '__main__':
    make_index()
    
