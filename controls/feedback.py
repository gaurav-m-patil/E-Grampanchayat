from flask import *
import os
from wtforms import *
import base64
import mysql.connector

class feedback(object):
	"""docstring for users"""
	def __init__(self):
		print("This is init Feedback")

	_conn = mysql.connector.connect(user='root',password='root',host='localhost',database='flask_egram',port=3306)
	_crsr = _conn.cursor()

	
	def AddFeedback(self,u_id,date,desc):
		self.u_id = u_id
		self.fb_date = date
		self.fb_desc = desc
		self._crsr.execute("INSERT INTO feedback (u_id,fb_date,fb_desc) VALUES (%s,%s,%s);",(self.u_id,self.fb_date,self.fb_desc))
		return True

	def SelectUserFB(self,u_id):
		self.u_id = u_id
		self._crsr.execute("SELECT * FROM feedback WHERE u_id = %s ORDER BY fb_date DESC",[self.u_id])
		result = self._crsr.fetchall()
		return result

	def SelectAll(self):
		self._crsr.execute("SELECT f.*,u.u_email,u.u_photo FROM feedback f JOIN users u WHERE f.u_id = u.u_id ORDER BY f.fb_date DESC;")
		result = self._crsr.fetchall()
		return result