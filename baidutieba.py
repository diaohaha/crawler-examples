#!usr/bin/env python
# -*- coding: utf-8 -*- 

#filename:baidutiba_paqu
#author:gaoda
#date:2013.6.5
#describe:从百度贴吧获取帖子

import pymongo
import httplib2
from sgmllib import SGMLParser

IO=0
IN=0

#贴吧页面类
class tieba(SGMLParser):
  def __init__(self):
		self.i=0
		SGMLParser.__init__(self)
		self.is_tieziid=""
		self.tiezi_id=[]
		self.is_end=False
	def start_a(self,attrs):
		tiezi_class=[v for k,v in attrs if k=='class']
		href=[v for k,v in attrs if k=='href']
		if tiezi_class:
			if tiezi_class[0]=="j_th_tit":
				self.tiezi_id.extend(href)
		if tiezi_class:
			if tiezi_class=="next":                                        #判断有无下一页
				self.is_end=False
				self.i=1
			if self.i==0:
				self=True			


#帖子页面类
class tiezi(SGMLParser):
	def __init__(self):
		SGMLParser.__init__(self)
		self.title=""
		self.is_title=""
		self.is_content=""
		self.reply_content=[]
		self.reply_time=[]
		self.reply_user_name=[]
		self.reply_user_id=[]
	def start_div(self,attrs):
		#获取用户名，id，回复时间，判断是否为回复内容
		temp_class=[v for k,v in attrs if k=='class']
		temp_data=[v for k,v in attrs if k=='data-field']
		if temp_class:
			if temp_class[0]=="l_post noborder" or temp_class[0]=="l_post ":
				#将字符串转换为dict
				temp1=str(temp_data[0])
				temp1=temp1.replace('true','1')
				temp1=temp1.replace('false','0')
				temp2=eval(temp1)
				try:
					self.reply_user_id.extend([temp2["author"]["id"]])#列表类型
					self.reply_user_name.extend([temp2["author"]["name"]])
					self.reply_time.extend([temp2["content"]["date"]])
				except:
					pass	
			if temp_class[0]=="d_post_content j_d_post_content":
				#判定回复
				self.is_content=1
	def start_br(self,attrs):
		self.is_content=""			
	def start_title(self,attrs):
		self.is_title=1
	def end_title(self):
		self.is_title=""	
	def end_div(self):
		self.is_content=""
	def handle_data(self,text):
		if text!='"':
			if self.is_content==1:
				if text:
					#print text.decode('gbk').encode('utf8')
					self.reply_content.append(text)
		else:
			self.is_content=""				
		if self.is_title==1:
			self.title=text					

#打开连接，连接复用
def open_connection():
	http=httplib2.Http()
	#resp,conn=http.request('www.tieba.baidu.com')
	return http

#数据存入mongo
def save_content(content):
	connection=pymongo.Connection("localhost",27017)
	db=connection.mydb
	tieba_emeishan=db.tieba_emeishan4
	tieba_emeishan.insert(content)

#取回复函数，返回回复
def get_content(http,url_id):
	content=[]
	is_end=0
	pn=1
	global tiezi
	global IO
	while is_end!=1:
		#print "读取页面:"
		tiezi_url='http://tieba.baidu.com'+url_id+'?pn='+str(pn)
		#print tiezi_url
		resp,conn=http.request(tiezi_url)
		if IO==0:	
			tiezi = tiezi()
			IO=1
		else:
			tiezi.__init__()					
		tiezi.feed(conn)
		i=0
		i_time=0
		i_content=0
		for a in tiezi.reply_content:
			i_time=i_time+1
		for a in tiezi.reply_time:
			i_content=i_content+1
		j=min(i_time,i_content)				
		while i<j:
			#print reply.decode('gbk').encode('utf8')
			try:
				content={}
				content["title"]=tiezi.title.decode('gbk').encode('utf8')
				replys={}
				replys["time"]=tiezi.reply_time[i].decode('gbk').encode('utf8')
				replys["name"]=tiezi.reply_user_name[i].decode('gbk').encode('utf8')
				replys["id"]=tiezi.reply_user_id[i]
				replys["content"]=tiezi.reply_content[i].decode('gbk').encode('utf8')
				content["reply"]=replys
			except:
				pass	
			i=i+1
			save_content(content)
		pn=pn+1	
		print "读取帖子:",tiezi.title.decode('gbk').encode('utf8')
		if tiezi.title.decode('gbk').encode('utf8')=="百度贴吧":
			is_end=1
	

				
#取帖子函数
def get_tiezi(http):
	url='http://tieba.baidu.com/f?kw=%B6%EB%C3%BC%C9%BD&tp=0&pn='
	pn=16550
	is_end=0
	global tieba
	global IN
	while not is_end:
		tieba_url=url+str(pn)
		print "**************************************************************"
		print "第",pn/50+1,"页"
		print "**************************************************************"
		#print tieba_url
		resp,conn=http.request(tieba_url)
		if IN==0:
			tieba=tieba()
			IN=1
		else:
			tieba.__init__()			
		tieba.feed(conn)	
		for tiezi_url in tieba.tiezi_id:
			get_content(http,tiezi_url)
		pn=pn+50
		is_end=tieba.is_end
		
#
if __name__=="__main__":
	http=open_connection()
	get_tiezi(http)
