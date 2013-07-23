# -*- coding: utf-8 -*-
from twisted.internet.protocol import Factory,Protocol
from twisted.internet import reactor
import urllib
import json
import string
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )


class my_protocol(Protocol):
	def __init__(self):
		print ""
	def __del__(self):
		print ""
	def connectionMade(self):
		print "connected"
	def connectionLost(self,reason):
		print "connection lost"
		print ""
	def dataReceived(self,data):
		if data=='quit':
			print "data received:%s"%(data)
			self.transport.loseConnection()
		else:	
			print "data received:%s"%(data)
			key=data.split("_")[0] 
			start=data.split("_")[1] 
			count=data.split("_")[2]
			url = "http://api.douban.com/v2/movie/search?q="+key+"&start="+start+"&count="+count
			page=urllib.urlopen(url)
			data=page.read()
			ddata=json.loads(data)
			j=int(start)
			i=0
			while j < int(count)+int(start):
				temp_title=ddata["subjects"][i]["title"]
				temp_avg=ddata["subjects"][i]["rating"]["average"]
				temp_collect=ddata["subjects"][i]["collect_count"]
				temp_subtype=ddata["subjects"][i]["subtype"]
				temp_year=ddata["subjects"][i]["year"]
				temp=temp_title+"_"+str(temp_collect)+"_"+str(temp_avg)+"_"+temp_subtype+"_"+str(temp_year)+"~"
				print temp
				self.transport.write(str(temp))
				#self.sendLine(str(temp))
				i=i+1
				j=j+1


f=Factory()
f.protocol=my_protocol
reactor.listenTCP(8080,f)

reactor.run()					
