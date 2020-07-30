from flask import *
from wtforms import *
import base64
import mysql.connector
import time

class operatorclass():

	_conn = mysql.connector.connect(user='root',password='root',host='localhost',database='flask_egram',port=3306)
	_crsr = _conn.cursor()

	def __init__(self):
		print("This is init admin")

	def encode(self,key, string):
	    encoded_chars = []
	    for i in range(len(string)):
	        key_c = key[i % len(key)]
	        encoded_c = chr(ord(string[i]) + ord(key_c) % 256)
	        encoded_chars.append(encoded_c)
	    encoded_string = "".join(encoded_chars)
	    return base64.urlsafe_b64encode(encoded_string.encode())

	def count(self):
		self._crsr.execute("SELECT COUNT(u_id) FROM users")
		users = self._crsr.fetchall()
		self._crsr.execute("SELECT COUNT(req_id) FROM user_request")
		users += self._crsr.fetchall()
		self._crsr.execute("SELECT COUNT(fb_id) FROM feedback")
		users += self._crsr.fetchall()
		return users


	def Login(self,op_email,op_password):
		self.op_email = op_email
		self.op_password = op_password

		self._crsr.execute("SELECT * FROM admin WHERE op_email = %s ;",[self.op_email])
		Data = self._crsr.fetchall()
		for data in Data:
			if data[2] == self.op_email and str(self.encode("9967589229",self.op_password)) == data[3]:
				return data[1]
		else:
			return False

	def Register(self,Name,uemail,upassword)	:
		self.name = Name
		self.email = uemail
		self.password = str(self.encode("9967589229",upassword))

		self._crsr.execute("SELECT * FROM admin")
		Data = self._crsr.fetchall()
		count = 0
		for data in Data :
			if data[3] == self.email or data[2] == self.email:
				count = 1
				break
		if count == 1:
			return False
		else:
			self._crsr.execute("INSERT INTO admin(op_name,op_email,op_password) VALUES(%s,%s,%s)",(self.name,self.email,self.password))
			return True

	def BackUp(self):
		current_time = time.strftime('%Y/%m/%d')
		optr = operatorclass()
		