from flask import *
import os
from wtforms import *
import base64
import mysql.connector

class updates():
	_conn = mysql.connector.connect(user='root',password='root',host='localhost',database='flask_egram',port=3306)
	_crsr = _conn.cursor()

	def __init__(self):
		print("This is init updates")

	def AllUpdates(self):
		self._crsr.execute("SELECT * FROM updates u join updates_category uc WHERE u.up_cat_id = uc.up_cat_id;")
		up_list = self._crsr.fetchall()
		return up_list

	def AllCategory(self):
		self._crsr.execute("SELECT * FROM updates_category;")
		category = self._crsr.fetchall()
		return category

	def uploadfile(self,file):
		APP_ROOT = os.path.dirname(os.path.abspath(__file__))
		target = os.path.join(APP_ROOT,'../static/updates_files/')
		print(target)
		filename = file.filename
		print(target)	
		destination = "/".join([target,filename])
		print(destination)
		file.save(destination)
		return filename

	def AddUpdates(self,title,date,category,file):
		self.up_title = title
		self.up_date = date
		self.up_cat_id = category
		self.up_file = file
		self.up_file_path = self.uploadfile(self.up_file)
		self._crsr.execute("INSERT INTO updates(up_title,up_date,up_cat_id,up_file_path) VALUES(%s,%s,%s,%s)",(self.up_title,self.up_date,self.up_cat_id,self.up_file_path))
		return True

	def AddCategory(self,cat_name):
		self._crsr.execute("INSERT INTO updates_category(up_cat_name) VALUES(%s);",[cat_name])
		return True

	def EditUpdates(self,id,title):
		self.up_id = id
		self.up_title = title
		self._crsr.execute("UPDATE updates SET up_title=%s WHERE up_id=%s",(self.up_title,self.up_id))
		return True

	def DeleteUpdates(self,id):
		self.up_id = id
		self._crsr.execute("DELETE FROM updates WHERE up_id = %s",[self.up_id])
		return True

	def SelectOneCate(self,cat_id):
		self.up_cat_id = cat_id
		self._crsr.execute("SELECT * FROM updates u join updates_category uc WHERE u.up_cat_id = uc.up_cat_id AND u.up_cat_id = %s",[self.up_cat_id])
		result = self._crsr.fetchall()
		return result