from flask import *
import os
from wtforms import *
import base64
import mysql.connector

class certi(object):
	"""docstring for users"""
	def __init__(self):
		print("This is init Certi")

	_conn = mysql.connector.connect(user='root',password='root',host='localhost',database='flask_egram',port=3306)
	_crsr = _conn.cursor()


	def AddFeedback(self,u_id,date,desc):
		self.u_id = u_id
		self.fb_date = date
		self.fb_desc = desc
		self._crsr.execute("INSERT INTO feedback (u_id,fb_date,fb_desc) VALUES (%s,%s,%s);",(self.u_id,self.fb_date,self.fb_desc))
		return True

	def SelectId(self,c_id):
		self.c_id = c_id
		self._crsr.execute("SELECT * FROM certis WHERE c_id = %s ",[self.c_id])
		result = self._crsr.fetchall()
		return result

	def SelectAll(self):
		self._crsr.execute("SELECT* FROM certis;")
		result = self._crsr.fetchall()
		return result
