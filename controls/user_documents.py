from flask import *
import os
from wtforms import *
import base64
import mysql.connector

class user_documents(object):
	"""docstring for users"""
	def __init__(self):
		print("This is init user_documents")

	_conn = mysql.connector.connect(user='root',password='root',host='localhost',database='flask_egram',port=3306)
	_crsr = _conn.cursor()

	def uploadfile(self,doc):
		APP_ROOT = os.path.dirname(os.path.abspath(__file__))
		target = os.path.join(APP_ROOT,'../static/user_documents/')
		print(target)
		filename = doc.filename
		print(filename)
		destination = "/".join([target,filename])
		print(destination)
		doc.save(destination)
		return filename

	def UploadDocument(self,req_id,filetype,file):
		self.req_id = req_id
		self.filetype = filetype
		self.file = self.uploadfile(file)
		self._crsr.execute("INSERT INTO user_document(req_id,ud_file_type,ud_file_path) values (%s,%s,%s)",(self.req_id,self.filetype,self.file))
		return True

	def selectDocument(self,req_id):
		self.u_id = session['u_id']
		self.req_id = req_id
		self._crsr.execute("SELECT * FROM user_document WHERE req_id = %s;",[req_id])
		docs = self._crsr.fetchall()
		return docs

	def selectAll(self):
		self._crsr.execute("SELECT * FROM user_document;")
		docs = self._crsr.fetchall()
		return docs

	def deleteDoc(self,req_id):
		self.req_id = req_id
		self._crsr.execute("delete * from user_document whare req_id = %",[req_id])
		return True
