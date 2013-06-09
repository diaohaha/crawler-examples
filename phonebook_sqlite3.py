#! /usr/bin/env python
# -*- coding: utf-8 -*-

#date:2012.6.6
 
from sqlalchemy import *
from sqlalchemy.orm import *
import string
import sys

#建立引擎
engine = create_engine('sqlite:////home/gd/python/mydb.db')

#类定义
class person(object):
  def _init_(self,id,name,sex,email,address,isphone):
		self.id=id
		self.name=name
		self.sex=sex
		self.email=email
		self.address=address
		self.isphone=isphone
class phone(object):
	def _init_(self,phone,id):
		self.phone=phone
		self.id=id
		
#建立映射
metadata=MetaData(engine)
personinfo_table = Table('personinfo', metadata,  
	Column('id', String, primary_key=True),  
	Column('name', String),  
	Column('sex', String),  
	Column('email', String),
	Column('address', String),
	Column('isphone', String)
)  
phone_table = Table('phone', metadata,  
	Column('phone', String, primary_key=True),  
	Column('id', String , ForeignKey('personinfo.id'))
)  
metadata.create_all(engine)
mapper(person , personinfo_table)
mapper(phone,phone_table)

#session对象连接引擎
session=sessionmaker(bind=engine)
session=create_session()

#查看
def look():
	i=0
	print "id".rjust(10),"|","name".rjust(10),"|","sex".rjust(6),"|","address".rjust(8),"|","email".rjust(18),"|","phone".rjust(10),"|"
	print "******************************************************************************"
	for temp_person,temp_phone in session.query(person,phone).join(phone,person.id==phone.id).all():
		print temp_person.id.rjust(10),"|",temp_person.name.rjust(10),"|",temp_person.sex.rjust(6),"|",temp_person.address.rjust(8),"|",temp_person.email.rjust(18),"|",temp_phone.phone.rjust(10),"|"
		i=i+1	
	if i=='0':
		print "no record!"

#插入
def add():
	temp_person=person()
	id2=temp_person.id=raw_input("please input id:")
	temp_person.name=raw_input("please input name:")
	temp_person.sex=raw_input("please input sex(male or female):")
	temp_person.email=raw_input("please input emial:")
	while '@' not in temp_person.email or '.com' not in temp_person.email :
		temp_person.email=raw_input("ERROR! please input emial again:")
	temp_person.address=raw_input("please input address:")
	temp_person.isphone=raw_input("is the person have a phone(yes or no):")
	i=temp_person.isphone
	session.add(temp_person)
	while i=='yes':
		temp_phone=phone()
		temp_phone.phone=raw_input("please input the phone number:")
		while not temp_phone.phone.isdigit():
			temp_phone.phone=raw_input("not a number,please try again:")
		temp_phone.id=id2
		session.add(temp_phone)
		i=raw_input("is he have other phone?(yes/no)")
	if(temp_person in session):
		print "add success!!"
	session.flush()
	

	
#删除
def delete():
	i=raw_input("1.delete person information\n2.delete phonenumber only\n3.return home\nplease choose a command:")
	if i=='1':
		temp_name=raw_input("please input the person name:")
		sign=0
		for temp_person in session.query(person).filter_by(name=temp_name).all():
			sign=sign+1
			session.delete(temp_person)
		if sign==0:
			print "no this record! delete failed!"	
		else:
			print "delete successful!"	
	elif i=='2':
		temp_phonenumber=raw_input('please input the phonenumber:')
		sign=0
		for temp_phone in session.query(phone).filter_by(phone=temp_phonenumber).all():
			sign=sign+1
			session.delete(temp_phone)
		if sign==0:
			print "no this record! delete failed!"	
		else:
			print "delete successful!"
	elif i=='3':
		print ""
	else:
		print "please choose a opertion!"
	session.flush()	
		
#修改
def change():
	print "1.change person information\n2.change phonenumber\n3.return home "
	i=raw_input("please choose a command:")
	if i=='1':
		temp_name=raw_input("please input the person name:")
		sign=0
		for temp_person in session.query(person).filter_by(name=temp_name).all():
			j=True
			sign=sign+1
			while j:
				print "***************************************************** "
				print "1.id  2.name  3.sex 4.address 5.email 0.return"
				print "***************************************************** "
				cmd = raw_input('pelase input the cloumn want you change:')
				if cmd=='2':
					temp_person.name=raw_input("input the new name:")
				elif cmd=='1':
					temp_person.id=raw_input("input the new id:")
				elif cmd=='3':
					temp_person.sex=raw_input("input the new sex:")
				elif cmd=='4':
					temp_person.address=raw_input("input the new address:")
				elif cmd=='5':
					temp_person.email=raw_input("input the new email:")				
				elif cmd=='0':
					j=False
				else:
					print ("please choose a cloumn!")
		if sign==0:
			print "no this record!"
		else:
			print "change successful!"				
	elif i==2:
		temp_phonenumber=raw_input("please input the id:")
		sign=0
		for temp_phone in session.query(phone).filter_by(phone=temp_phonenumber).all():
			sign=sign+1 
			temp_phone=raw_input("please input the new phone number:")
		if sign==0:
			print "no this record!"
		else:
			print "change successful!"
	elif i==3:
		print ""
	else:
		print "input error!! please reinput:"
	session.flush()


#查找
def find():
	temp=raw_input("please input the key words:")	
	i=0
	print "id".rjust(10),"|","name".rjust(10),"|","sex".rjust(6),"|","address".rjust(8),"|","email".rjust(18),"|","phone".rjust(10),"|"
	print "******************************************************************************"
	for temp_person,temp_phone in session.query(person,phone).join(phone,person.id==phone.id).filter(or_(person.id==temp,person.name==temp,person.sex==temp,person.email==temp,person.address==temp,phone.phone==temp)).all():
		print temp_person.id.rjust(10),"|",temp_person.name.rjust(10),"|",temp_person.sex.rjust(6),"|",temp_person.address.rjust(8),"|",temp_person.email.rjust(18),"|",temp_phone.phone.rjust(10),"|"
		i=i+1
	if i==0:
		print "no record!"
	

#main
print '''********************************************************************* 
                       phonebook2.0
********************************************************************* 
   1.Look   2.Add  3.Delete  4.Change   5.Find  6.Exit
********************************************************************* ''' 
running = True			
while running:
    cmd = raw_input('Input a Command: ')
    if cmd == '1' :
        look()
        print "****************************************************************************" 
    elif cmd == '2' :
		add()
		print "****************************************************************************" 
    elif cmd == '6' :
        running = False
        print "****************************************************************************" 	
    elif cmd == '3' :
		delete()
		print "****************************************************************************" 
    elif cmd == '4' :
		change()
		print "****************************************************************************" 
    elif cmd == '5' :
		find()
		print "****************************************************************************" 
    else:
        print "*********************************************************************" 
        print "Please input a command!"
print "Thank you for using!"

