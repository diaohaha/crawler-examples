#!usr/bin/env python
# -*- coding: utf-8 -*-

#filename:make_index
#author:gaoda
#date:2013.6.9
#describe:建立json格式索引

import json
import xapian
import jieba



dbfile=file("tieba.json")
dat=dbfile.read()
datas=dat.split('\n')
ddatas=[]
for data in datas:
	a=eval(data)
	ddatas.append(a)
#print ddatas
dbfile.close()	
