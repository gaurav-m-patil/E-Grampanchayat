from flask import *
import os
from wtforms import *
import base64
import mysql.connector
import time
import random
import controls.certi as certi
import controls.user_documents as u_d
import smtplib

current_time = time.strftime('%Y/%m/%d')

class user_request(object):

    _conn = mysql.connector.connect(user='root',password='root',host='localhost',database='flask_egram',port=3306)
    _crsr = _conn.cursor()

    """docstring for users"""

    def __init__(self):
        print("This is init user_request")

    def NewReq(self,c_id):
        self.c_id = c_id
        self.u_id = session['u_id']
        self.c_date = current_time
        self.status = "Not Complete"
        self.t_id = random.randint(1000,100000)
        self._crsr.execute("SELECT tracking_id FROM user_request;")
        data = self._crsr.fetchall()
        print(data)
        while True:
            if self.t_id not in data:
                session['t_id'] = self.t_id
                self.zero = '0'
                self._crsr.execute("INSERT INTO user_request(u_id,c_id,req_date,req_status,tracking_id,status) VALUES (%s,%s,%s,%s,%s,%s);",(self.u_id,self.c_id,self.c_date,self.status,self.t_id,self.zero))
                break
            else:
                self.t_id = random.randint(1000,100000)
        return True

    def SelectReq(self,t_id):
        self.t_id = t_id
        self._crsr.execute("SELECT u_req.req_id,u_req.u_id,u_req.c_id,req_date,req_status,tracking_id,c_name,u_first_name,u_middle_name,u_last_name,u_mobile,u_email,u_reg_date,u_aadhar_no,u_dob,u_gender,u_address,u_pin_code,u_districts,u_occupation,u_photo,u_income FROM user_request as u_req join certis as u_c on u_req.c_id = u_c.c_id join users as u on u_req.u_id =u.u_id WHERE tracking_id = %s;",[self.t_id])
        data = self._crsr.fetchall()
        return data


    def Submit(self,req_id):
        self._crsr.execute("UPDATE user_request SET req_status = %s WHERE req_id = %s",("Submitted",req_id))
        return True

    def Select_all(self):
        self._crsr.execute("SELECT * FROM user_request as u_req join certis as u_c on u_req.c_id = u_c.c_id WHERE u_id = %s",[session['u_id']])
        reqs = self._crsr.fetchall()
        return reqs

    def SelectAll(self):
        self._crsr.execute("SELECT * FROM user_request as u_req join certis as u_c on u_req.c_id = u_c.c_id join users as u on u_req.u_id =u.u_id order by req_date DESC;")
        reqs = self._crsr.fetchall()
        return reqs

    def DeleteReq(self,req_id):
        u_d.deleteDoc(req_id)
        self._crsr.execute("delete * from user_request whare req_id = %",[req_id])
        return True

    def uploadfile(self,photo):
        APP_ROOT = os.path.dirname(os.path.abspath(__file__))
        target = os.path.join(APP_ROOT,'../static/images/')
        filename = photo.filename
        destination = "/".join([target,filename])
        photo.save(destination)
        return filename

    def verifyReq(self,req_id,date):        
        self._crsr.execute("update user_request set req_status = 'Completed', status = 1, verify_date = %s where req_id= %s",(date,req_id))
        return "Verified"
    
    def SendMail(self,req_id,t_id,u_email):
        message = """
This is HTML message.
This is headline.
Message from Egram.
Certificate Link http://127.0.0.1:5000/CreateDoc?t_id="""+t_id+"""
"""
        
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login("sandyunique75@gmail.com","Sandy@75")
        server.sendmail("sandyunique75@gmail.com", u_email, message)
        server.quit()
        
        return True
