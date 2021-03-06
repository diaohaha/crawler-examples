#!usr/bin/env python
# -*- coding: utf-8 -*- 
#filename:twisted_tcp_client
#author:gaoda
#date:2013.6.4


from twisted.internet import reactor,defer,protocol
from sqlalchemy import *
from sqlalchemy.orm import *
import string
import json
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )


#sqlite3数据库
#建立引擎
engine = create_engine('sqlite:///my2db.db')#使用相对路径打开数据库

#类定义
class movie(object):
	def _init_(self,title,collect,avggrade,subtype,year):
		self.title=title
		self.collect=collect
		self.avggrade
		self.subtype
		self.year=year

		
#建立映射
metadata=MetaData(engine)
moive_table = Table('moive', metadata,  
	Column('title', String, primary_key=True),  
	Column('collect', String),  
	Column('avggrade', String),  
	Column('subtype', String),
	Column('year', String)
)  

metadata.create_all(engine)
mapper(movie , moive_table)


#session对象连接引擎
session=sessionmaker(bind=engine)
session=create_session() 

global j

#teisted 客户端
class myclientprotocol(protocol.Protocol):
	def connectionMade(self):
		print "connected"
		temp_serach=raw_input("输入关键词:")
		temp_bnum=raw_input("输入开始数:")
		temp_num=raw_input("输入总数:")
		temp=temp_serach+"_"+temp_bnum+"_"+temp_num
		self.transport.write(temp)
	def dataReceived(self,data):
		data2=data.split("~")
		i=0
		j=len(data2)-1
		while i<j:
			temp_movie=movie()
			temp_movie.title=unicode(data2[i].split("_")[0]) 
			temp_movie.collect=data2[i].split("_")[1]
			temp_movie.avggrade=data2[i].split("_")[2]
			temp_movie.subtype=data2[i].split("_")[3]
			temp_movie.year=data2[i].split("_")[4] 
			session.add(temp_movie) 
			print data2[i]
			i=i+1
		#self.transport.loseConnection()
		self.transport.write('quit')
		session.flush()
		self.transport.loseConnection()
		
		 

class myclientfactory(protocol.ClientFactory):
    protocol=myclientprotocol
    def clientConnectionLost(self,transport,reason):
        reactor.stop()
    def clientConnectionFailed(self,transport,reason):
        print reason.getErrorMessage()
        reactor.stop()


#main
def main():
	a=0
	while True:
		cmd=raw_input( "input a command:")
		if cmd=='1':
			i=0
			print "|","收藏数".rjust(13),"|","平均分".rjust(6),"|","类型".rjust(9),"|","年份".rjust(8),"|","电影名".rjust(10),"|"
			print "******************************************************************************"
			for temp_movie in session.query(movie).all():
				print "|",temp_movie.collect.rjust(10),"|",temp_movie.avggrade.rjust(6),"|",temp_movie.subtype.rjust(8),"|",temp_movie.year.rjust(6),"|",temp_movie.title.rjust(10)
				i=i+1	
			if i=='0':
				print "no record!"
			print "******************************************************************************"	
		elif cmd=='2':
			if a==0:
				reactor.connectTCP(host,port,myclientfactory())
				reactor.run()
				a=1
			else:
				reactor.connectTCP(host,port,myclientfactory())	
		elif cmd=='3':
			break
		else:
			print "input error! reput:"	
	print "thank you for using!"	       


if __name__=="__main__":
    host="127.0.0.1"
    port=8080
    print "****************************************************************************"
    print "                            豆瓣api 1.0      "
    print "****************************************************************************"
    print "                     1.历史记录"
    print "                     2.电影查询"
    print "                     3.退出"
    print "****************************************************************************"
    main()   

