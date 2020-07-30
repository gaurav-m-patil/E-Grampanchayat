
from flask import *
import sys
import os
#sys.path.insert(0,"/home/sidd/Projects/Py/egrampanchayat/controls")
from controls.operatorclass import operatorclass
from controls.users import users
from controls.area import area
from controls.updates import updates
from controls.feedback import feedback
from controls.certi import certi
from controls.user_request import user_request
from controls.user_documents import user_documents
import time
import pdfkit
from wtforms import *
import base64
import mysql.connector


app = Flask(__name__)
current_time = time.strftime('%Y/%m/%d')
optr = operatorclass()
user = users()
area = area()
updates = updates()
feedback = feedback()
certi = certi()
u_req = user_request()
u_doc = user_documents()

@app.route('/')
def index():
	return render_template("home.html")

def encode(key, string):
    encoded_chars = []
    for i in range(len(string)):
        key_c = key[i % len(key)]
        encoded_c = chr(ord(string[i]) + ord(key_c) % 256)
        encoded_chars.append(encoded_c)
    encoded_string = "".join(encoded_chars)
    return base64.urlsafe_b64encode(encoded_string.encode())


""" Main Routes """

@app.route('/locations',methods=['GET'])
def locations():
	category = request.args.get('cat')
	data = area.SelectOne(category)
	allcat = area.AllCategory()
	return render_template('locations.html',data=data,cat=allcat)


@app.route('/update',methods=['GET'])
def update():
	category = request.args.get('cat')
	if category:
		up_list = updates.SelectOneCate(category)
		up_cate = updates.AllCategory()
		return render_template("updates.html",data=up_list,up_cate=up_cate)
	else:
		up_list = updates.AllUpdates()
		cate = updates.AllCategory()
		return render_template("updates.html",data=up_list,up_cate=cate)

""" End Main Routes """



""" User registration """

@app.route('/user_registration',methods=['GET','POST'])
def user_register():
	if request.method == 'POST':
		first_name = request.form['first_name']
		middle_name = request.form['middle_name']
		last_name = request.form['last_name']
		mobile = request.form['mobile']
		email = request.form['email']
		password = request.form['password']
		c_password = request.form['c_password']
		reg_date = current_time
		aadhar_no = request.form['aadhar_no']
		dob = request.form['dob']
		gender = request.form['gender']
		address = request.form['address']
		pin_code = request.form['pin_code']
		district = request.form['district']
		occu = request.form['occu']
		photo = request.files['photo']
		if password == c_password:
			result = user.Register(first_name,middle_name,last_name,mobile,email,password,reg_date,aadhar_no,dob,gender,address,pin_code,district,occu,photo)
		else:
			flash('Password Not Match', 'success')
			redirect(url_for('user_register'))

		if result == True:
			flash('You are Registration Success... now goto login', 'success')
			redirect(url_for('login'))
		else:
			flash('User Is Alrady Exist', 'success')
			redirect(url_for('index'))

	return render_template('userregistration.html',form=form)

"""  End User registration """


""" User Login """

@app.route('/login',methods=['GET','POST'])
def login():
	if request.method == 'POST':
		email = request.form['email']
		user_pass = request.form['password']

		result = user.Login(email,user_pass)
		if result == True:
			message = "Password Match"
			return render_template('user/user_home.html',msg=message)
		else:
			error = "Username or Password Not Match"
			return render_template('login.html',error=error)
	else:
		return render_template('login.html')

""" End User Login """

""" User Routes """

@app.route('/userHome')
def userHome():
	if session.get('loggedIn') == True:
		return render_template('user/user_home.html')
	else:
		return redirect(url_for('login'))

@app.route('/user_logout')
def user_logout():
   # remove the username from the session if it is there
   session.pop('u_id',None)
   session.pop('u_email',None)
   session.pop('u_full_name', None)
   session.pop('loggedIn',None)
   return redirect(url_for('index'))

@app.route('/user_profile')
def user_profile():
	if session.get('loggedIn') == True:
		data = user.SingleUser()
		return render_template('user/user_profile.html',data=data)
	else:
		return redirect(url_for('login'))

@app.route('/user_update',methods=['GET','POST'])
def user_update():
	if session.get('loggedIn') == True:
		data = user.SingleUser()
		if request.method == 'POST':
			first_name = request.form['first_name']
			middle_name = request.form['middle_name']
			last_name = request.form['last_name']
			mobile = request.form['mobile']
			email = request.form['email']
			aadhar_no = request.form['aadhar_no']
			dob = request.form['dob']
			gender = request.form['gender']
			address = request.form['address']
			pin_code = request.form['pin_code']
			district = request.form['district']
			occu = request.form['occu']
			photo = request.files['photo']

			result = user.Update(first_name,middle_name,last_name,mobile,email,aadhar_no,dob,gender,address,pin_code,district,occu,photo)

			if result == True:
				flash('Your Updation Successfully Done', 'success')
				redirect(url_for('index'))
			else:
				flash('Somwthing went wrong', 'success')
				redirect(url_for('index'))
		return render_template('user/user_update.html',form=form,data=data)
	else:
		return redirect(url_for('login'))

@app.route('/user_locations',methods=['GET'])
def user_locations():
	if session.get('loggedIn') == True:
		category = request.args.get('cat')
		data = area.SelectOne(category)
		allcat = area.AllCategory()
		return render_template('user/user_locations.html',data=data,cat=allcat)
	else:
		return redirect(url_for('login'))


@app.route('/user_letest',methods=['GET'])
def user_letest():
	if session.get('loggedIn') == True:
		category = request.args.get('cat')
		if category:
			up_list = updates.SelectOneCate(category)
			up_cate = updates.AllCategory()
			return render_template("user/user_letest.html",data=up_list,up_cate=up_cate)
		else:
			up_list = updates.AllUpdates()
			cate = updates.AllCategory()
			return render_template("user/user_letest.html",data=up_list,up_cate=cate)
	else:
		return redirect(url_for('login'))

@app.route('/user_feedback',methods=['GET','POST'])
def user_feedback():
	if session.get('loggedIn') == True:
		u_id = request.args.get('u_id')
		if request.method == 'POST':
			if request.form['fb_desc'] != "":
				result = feedback.AddFeedback(u_id,current_time,request.form['fb_desc'])
		fb_list = feedback.SelectUserFB(u_id)
		return render_template('user/user_feedback.html',data=fb_list)
	else:
		return redirect(url_for('login'))

@app.route('/user_request',methods=['GET','POST'])
def user_request():
	if session.get('loggedIn') == True:
		certis = certi.SelectAll()
		if request.method == "POST":
			c_id = request.form['c_id']
			submit = u_req.NewReq(c_id)
			if submit == True:
				return redirect(url_for('user_document',c_id=c_id))
			else:
				render_template('user/user_request.html',data=certis)
		return render_template('user/user_request.html',data=certis)
	else:
		return redirect(url_for('login'))

@app.route('/user_document',methods=['GET','POST'])
def user_document():
	if session.get('loggedIn') == True:
		id = request.args.get('c_id')
		crt =  certi.SelectId(id)
		u_detail = user.SingleUser()
		req = u_req.SelectReq(session['t_id'])
		docs = u_doc.selectDocument(req[0][0])
		return render_template('user/user_document.html',crt=crt,u_detail=u_detail,u_req=req,docs = docs)
	else:
		return redirect(url_for('login'))

@app.route('/user_income',methods=['GET','POST'])
def user_income():
	if session.get('loggedIn') == True:
		income = request.form['income']
		cid = request.form['c_id']
		result = user.UpdateIncome(income)
		return redirect(url_for('user_document',c_id=cid))
	else:
		return redirect(url_for('login'))

@app.route('/user_req_doc',methods=['GET','POST'])
def user_req_doc():
	if session.get('loggedIn') == True:
		filetype = request.form['filetype']
		file = request.files['u_doc']
		req_id = request.form['req_id']
		cid = request.form['c_id']
		doc = u_doc.UploadDocument(req_id,filetype,file)
		return redirect(url_for('user_document',c_id=cid))
	else:
		return redirect(url_for('login'))

@app.route('/submit_req',methods=['GET','POST'])
def submit_req():
	if session.get('loggedIn') == True:
		req_id = request.args.get('req_id')
		result = u_req.Submit(req_id)
		session.pop('t_id', None)
	return redirect(url_for('userHome'))

@app.route('/delete_req',methods=['GET','POST'])
def delete_req():
	if session.get('loggedIn') == True:
		req_id = request.args.get('req_id')
		u_req.DeleteReq(req_id)		
	return redirect(url_for('userHome'))

@app.route('/all_req')
def all_req():
	if session.get('loggedIn'):
		reqs = u_req.Select_all()
		return render_template('user/user_all_req.html',reqs=reqs)
	else:
		return redirect(url_for('login'))


""" End User Routes """

""" Operator Registration """

class Registration(Form):
    name = StringField(u'Full Name', validators=[validators.input_required()])
    email = StringField(u'Email Id', validators=[validators.input_required()])
    password = PasswordField(u'Password', validators=[validators.input_required(),validators.EqualTo('confirm',message='Password Not Match'),validators.Length(min=4,max=10)])
    confirm = PasswordField('confirm Password')

@app.route('/operator_register',methods=['GET','POST'])
def operator_register():
	form = Registration(request.form)
	if request.method == 'POST' and form.validate():
		name = form.name.data
		email = form.email.data
		password = form.password.data

		result = optr.Register(name,email,password)

		if result == True:
			flash('You are Registration Success... now goto login', 'success')
			redirect(url_for('index'))
		else:
			flash('User Is Alrady Exixt', 'success')
			redirect(url_for('index'))

	return render_template('register.html',form=form)

""" End Operator Registration """


""" Operator Login """

@app.route('/operator',methods=['GET','POST'])
def operatorLogin():
	if request.method == 'POST':
		op_email = request.form['op_email']
		op_password = request.form['op_password']

		result = optr.Login(op_email,op_password)

		if result:
			session['op_name'] = result
			session['logged_in'] = True
			return redirect(url_for('operatorHome'))
		else:
			error = "Username or Password Not Match"
			return render_template('operator/operatorLogin.html',error=error)
	else:
		return render_template('operator/operatorLogin.html')

""" End Operator Login """
""" Operators Routes """

@app.route('/operatorHome')
def operatorHome():
	if session.get('logged_in') == True:
		count = optr.count()
		cate_count = area.CountCategory()
		feedback_data = feedback.SelectAll()
		return render_template('operator/operatorHome.html',data=count,cate_count=cate_count,fb_data=feedback_data)
	else:
		return redirect(url_for('operatorLogin'))



@app.route('/newUser')
def newUser():
	if session.get('logged_in') == True:
		data = user.AllUsers()
		return render_template('operator/newUser.html',data=data)
	else:
		return redirect(url_for('operatorLogin'))


@app.route('/operatorTables')
def operatorTables():
	if session.get('logged_in') == True:
		return render_template('operator/operatorTables.html')
	else:
		return redirect(url_for('operatorLogin'))


@app.route('/services')
def services():
	if session.get('logged_in') == True:
		category = request.args.get('cat')
		if category:
			data = area.SelectOne(category)
			allcat = area.AllCategory()
			return render_template('operator/services.html',data=data,cate=allcat)
		else:
			data = area.SelectAll()
			cate = area.AllCategory()
			return render_template('operator/services.html',data=data,cate=cate)
	else:
		return redirect(url_for('operatorLogin'))



@app.route("/addArea",methods=['GET','POST'])
def addArea():
	if request.method == 'POST':
		a_category = request.form['a_category']
		a_name = request.form['a_name']
		a_address = request.form['a_address']
		a_contact = request.form['a_contact']
		a_email = request.form['a_email']
		result = area.AddNew(a_category,a_name,a_address,a_contact,a_email)
		if result == True:
			return redirect(url_for('services'))
		else:
			return redirect(url_for('services'))
	else:
		return redirect(url_for('services'))

@app.route("/updateArea",methods=['GET','POST'])
def updateArea():
	if request.method == 'POST':
		a_id = request.form['a_id']
		a_category = request.form['a_category']
		a_name = request.form['a_name']
		a_address = request.form['a_address']
		a_contact = request.form['a_contact']
		a_email = request.form['a_email']
		result = area.Update(a_id,a_category,a_name,a_address,a_contact,a_email)
		if result == True:
			return redirect(url_for('services'))
		else:
			return redirect(url_for('services'))
	else:
		return redirect(url_for('services'))


@app.route("/searchArea")
def searchArea():
	text = request.args['searchText']
	data = area.Search()
	values = []
	for d in data:
		values.append(d[2])
	print(values)
	result = [c for c in values if text.lower() in c.lower()]
	# return as JSON
	return json.dumps({"results":result})


@app.route("/deleteArea",methods=['GET','POST'])
def deleteArea():
	if request.method == 'POST':
		a_id = request.form['a_id']
		result = area.DeleteOne(a_id)
		return redirect(url_for('services'))
	return redirect(url_for('services'))

@app.route('/optr_logout')
def optr_logout():
   # remove the username from the session if it is there
   session.pop('op_name', None)
   session.pop('logged_in', None)
   return redirect(url_for('index'))


@app.route('/optr_updates')
def optr_updates():
	if session.get('logged_in') == True:
		up_list = updates.AllUpdates()
		cate = updates.AllCategory()
		return render_template("operator/updates.html",data=up_list,cate=cate)
	else:
		return redirect(url_for('operatorLogin'))

@app.route('/addUpdates',methods=['GET','POST'])
def addUpdates():
	if request.method == 'POST':
		up_cat_id = request.form['up_category']
		up_title = request.form['up_title']
		up_date = current_time
		up_file = request.files['up_file']
		result = updates.AddUpdates(up_title,up_date,up_cat_id,up_file)
	return redirect(url_for('optr_updates'))

@app.route('/editUpdates',methods=['GET','POST'])
def editUpdates():
	if request.method == 'POST':
		up_id = request.form['up_id']
		up_title = request.form['up_title']
		result = updates.EditUpdates(up_id,up_title)
	return redirect(url_for('optr_updates'))

@app.route('/addUpdatesCategory',methods=['GET','POST'])
def addUpdatesCategory():
	if request.method == 'POST':
		up_cat_name = request.form['cat_name']
		result = updates.AddCategory(up_cat_name)
	return redirect(url_for('optr_updates'))

@app.route('/deleteUpdates',methods=['GET'])
def deleteUpdates():
	up_id = request.args.get('up_id')
	result = updates.DeleteUpdates(up_id)
	return redirect(url_for('optr_updates'))

@app.route('/optr_feedback')
def optr_feedback():
	if session.get('logged_in') == True:
		fb_list = feedback.SelectAll()
		return render_template("operator/operatorFeedback.html",data=fb_list)
	else:
		return redirect(url_for('operatorLogin'))

@app.route('/newReq')
def newReq():
	if session.get('logged_in') == True:
		req_data = u_req.SelectAll()
		req_doc = u_doc.selectAll()
		return render_template("operator/newReq.html",req_data=req_data,req_doc=req_doc)
	else:
		return redirect(url_for('operatorLogin'))

@app.route('/CreateDoc')
def CreateDoc():	
	t_id = request.args.get('t_id')
	req_data = u_req.SelectReq(t_id)
	req_doc = u_doc.selectAll()
	if req_data[0][6] == 'Income Certificate':
		rendered = render_template("operator/CreateDocIncome.html",req_data=req_data,req_doc=req_doc,c_date = current_time)
		pdf = pdfkit.from_string(rendered, False)
		response = make_response(pdf)
		response.headers['Content-Type'] = 'application/pdf'
		response.headers['Content-Disposition'] = 'inline; filename = Certificate.pdf'
		return response
	elif req_data[0][6] == 'Birth Certificate':
		rendered = render_template("operator/CreateDocBirth.html",req_data=req_data,req_doc=req_doc,c_date = current_time)
		pdf = pdfkit.from_string(rendered, False)
		response = make_response(pdf)
		response.headers['Content-Type'] = 'application/pdf'
		response.headers['Content-Disposition'] = 'inline; filename = Certificate.pdf'
		return response

@app.route('/verifyDoc',methods=['GET','POST'])
def verifyDoc():
	if session.get('logged_in') == True:
		if request.method == 'POST':
			req_id = request.form['req_id']
			t_id = request.form['t_id']
			u_email = request.form['u_email']
			print(req_id)
			result = u_req.verifyReq(req_id,current_time)
			if result == "Verified":				
				mail = u_req.SendMail(req_id,t_id,u_email)
				if mail == True:
					return redirect(url_for('newReq'))
				else:
					return render_template("Email Not Send")
	else:
		return redirect(url_for('operatorLogin'))




""" End Operators Routes """



@app.route('/about')
def about():
	return render_template("about.html")


app.secret_key = 'sidd123'
if __name__ == '__main__':
	app.run(debug=True)
