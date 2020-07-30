from flask import *
import os
from wtforms import *
import base64
import mysql.connector

class users(object):
	"""docstring for users"""
	def __init__(self):
		print("This is init Usere")

	_conn = mysql.connector.connect(user='root',password='root',host='localhost',database='flask_egram',port=3306)
	_crsr = _conn.cursor()

	def encode(self,key, string):
	    encoded_chars = []
	    for i in range(len(string)):
	        key_c = key[i % len(key)]
	        encoded_c = chr(ord(string[i]) + ord(key_c) % 256)
	        encoded_chars.append(encoded_c)
	    encoded_string = "".join(encoded_chars)
	    return base64.urlsafe_b64encode(encoded_string.encode())

	def AllUsers(self):
		self._crsr.execute("SELECT * FROM users ORDER BY u_id ASC;")
		users = self._crsr.fetchall()
		return users

	def SingleUser(self):
		self.email = session['u_email']
		self._crsr.execute("SELECT * FROM users where u_email = %s ;",[self.email])
		user = self._crsr.fetchall()
		return user

	def Login(self,email,password):
		self.email = email
		self.password = str(self.encode("9967589229",password))

		self._crsr.execute("SELECT * FROM users WHERE u_email = %s ;",[self.email])
		Data = self._crsr.fetchall()
		for data in Data :
			if data[5] == self.email and self.password == data[6]:
				session['u_full_name'] = data[1]+" "+data[3]
				session['u_email'] = data[5]
				session['u_id'] = data[0]
				session['loggedIn'] = True
				return True
		else:
			return False

	def uploadfile(self,photo):
		APP_ROOT = os.path.dirname(os.path.abspath(__file__))
		target = os.path.join(APP_ROOT,'../static/images/')
		print(target)
		filename = photo.filename
		print(target)
		destination = "/".join([target,filename])
		print(destination)
		photo.save(destination)
		return filename

	def Register(self,first_name,middle_name,last_name,mobile,email,password,reg_date,aadhar_no,dob,gender,address,pin_code,district,occu,photo):
		self._crsr.execute("SELECT * FROM users")
		Data = self._crsr.fetchall()
		count = 0
		for data in Data :
			if data[8] == aadhar_no or data[5] == email:
				count = 1
				break
		if count == 1:
			return False
		else:
			self.u_photo = self.uploadfile(photo)
			self.status = "Active"
			self.password = str(self.encode("9967589229",password))
			self._crsr.execute("INSERT INTO users(u_first_name,u_middle_name,u_last_name,u_mobile,u_email,u_password,u_reg_date,u_aadhar_no,u_dob,u_gender,u_address,u_pin_code,u_districts,u_occupation,u_photo,u_status) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(first_name,middle_name,last_name,mobile,email,self.password,reg_date,aadhar_no,dob,gender,address,pin_code,district,occu,self.u_photo,self.status))
			return True

	def Update(self,first_name,middle_name,last_name,mobile,email,aadhar_no,dob,gender,address,pin_code,district,occu,photo):
		self._crsr.execute("SELECT * FROM users")
		Data = self._crsr.fetchall()
		count = 0
		for data in Data :
			if data[8] == aadhar_no or data[5] == email:
				count = 1
				break
		if count == 1:
			return False
		else:
			self.u_photo = self.uploadfile(photo)
			self.status = "Active"
			self._crsr.execute("UPDATE users SET u_first_name = %s,u_middle_name = %s,u_last_name = %s,u_mobile = %s,u_aadhar_no = %s,u_dob = %s,u_gender = %s,u_address = %s,u_pin_code = %s,u_districts = %s,u_occupation = %s,u_photo = %s WHERE u_email = %s",(first_name,middle_name,last_name,mobile,aadhar_no,dob,gender,address,pin_code,district,occu,self.u_photo,email))
			return True

	def UpdateIncome(self,income):
		update = self._crsr.execute("UPDATE users SET u_income= %s WHERE u_email = %s",(income,session['u_email']))
		return True
