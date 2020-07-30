from flask import *
import os
from wtforms import *
import base64
import mysql.connector

class area():
	_conn = mysql.connector.connect(user='root',password='root',host='localhost',database='flask_egram',port=3306)
	_crsr = _conn.cursor()

	def __init__(self):
		print("This is init Area")

	def AddNew(self,category,name,address,contact,email):
		self.a_category = category
		self.a_name = name
		self.a_address = address
		self.a_contact = contact
		self.a_email = email
		self._crsr.execute("INSERT INTO area(a_category,a_name,a_address,a_contact,a_email) VALUES(%s,%s,%s,%s,%s)",(self.a_category,self.a_name,self.a_address,self.a_contact,self.a_email))
		return True


	def Update(self,a_id,category,name,address,contact,email):
		self.a_id = a_id
		self.a_category = category
		self.a_name = name
		self.a_address = address
		self.a_contact = contact
		self.a_email = email
		self._crsr.execute("UPDATE area SET a_category = %s, a_name=%s, a_address = %s, a_contact = %s, a_email = %s WHERE a_id= %s;",(self.a_category,self.a_name,self.a_address,self.a_contact,self.a_email,self.a_id))
		return True	

	def SelectAll(self):
		self._crsr.execute("SELECT * FROM area;")
		area = self._crsr.fetchall()
		return area

	def Search(self):
		self._crsr.execute("SELECT * FROM `area`")
		result = self._crsr.fetchall()
		return result

	def AllCategory(self):
		self._crsr.execute("SELECT DISTINCT a_category FROM area;")
		category = self._crsr.fetchall()
		return category

	def CountCategory(self):
		self._crsr.execute("SELECT DISTINCT a_category FROM area;")
		categories = self._crsr.fetchall()
		count = []
		for category in categories:
			cat = category[0]
			self._crsr.execute("SELECT COUNT(a_id),a_category FROM area WHERE a_category = %s;",[cat])
			count.append(self._crsr.fetchall())
		return count

	def SelectOne(self,cate):
		self.category = cate
		self._crsr.execute("SELECT * FROM area WHERE a_category = %s;",[self.category])
		area = self._crsr.fetchall()
		return area

	def DeleteOne(self,id):
		self.a_id = id
		self._crsr.execute("DELETE FROM area WHERE a_id = %s;",[self.a_id])
		return "Success"
