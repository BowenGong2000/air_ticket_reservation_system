#Import Flask Library
from distutils.log import error
import email
from email import message
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors

#Initialize the app from Flask
app = Flask(__name__)

#Configure MySQL
conn = pymysql.connect(host='localhost',
					   port=8890,
                       user='root',
                       password='root',
                       db='air_ticket_reservation_system',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

# Define a route to the welcome page 
@app.route('/')
def hello():
	return render_template('welcome.html')

# Define a route to the customer register page 
@app.route('/c_register')
def c_register():
	return render_template('c_register.html')

# Define a route to the customer login page 
@app.route('/c_login')
def c_login():
	return render_template('c_login.html')

# Authenticates customer register
@app.route('/c_register_auth', methods=['GET', 'POST'])
def c_register_auth():
	# grabs information from the forms
	email = request.form['email']
	pswd = request.form['pswd']
	c_name = request.form['c_name']
	bd_num = request.form['bd_num']
	street = request.form['street']
	city = request.form['city']
	state = request.form['state']
	ph_num = request.form['ph_num']
	ppt_num = request.form['ppt_num']
	ppt_exp = request.form['ppt_exp']
	ppt_country = request.form['ppt_country']
	dob = request.form['dob']

	# cursor used to send queries
	cursor = conn.cursor()
	# executes 1query
	query = 'SELECT * FROM customer WHERE email = %s'
	cursor.execute(query, (email))
	# stores the results in a variable
	data = cursor.fetchone()
	# use fetchall() if you are expecting more than 1 data row
	error = None
	if (data):
		# If the previous query returns data, then user exists
		error = "This user already exists"
		return render_template('c_register.html', error=error)
	else:
		ins = 'INSERT INTO customer VALUES(%s, MD5(%s), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
		cursor.execute(ins, (email, pswd, c_name, bd_num, street, city, state, ph_num, ppt_num, ppt_exp, ppt_country, dob))
		conn.commit()
		cursor.close()
		return render_template('c_login.html')

# Authenticates customer login
@app.route('/c_login_auth', methods=['GET', 'POST'])
def c_login_auth():
	#grabs information from the forms
	email = request.form['email']
	pswd = request.form['pswd']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM customer WHERE email = %s and pswd = MD5(%s)'
	cursor.execute(query, (email, pswd))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None

	if(data):
		#creates a session for the the user
		#session is a built in
		session['email'] = email
		return redirect(url_for('c_homepage'))
	else:
		#returns an error message to the html page
		error = 'Invalid login or username'
		return render_template('c_login.html', error=error)

# Customer homepage

@app.route('/c_homepage')
def c_homepage():
	email = session['email']
	return render_template('c_homepage.html', username=email)

@app.route('/c_viewFlight')
def c_viewFlight():
	email = session['email']
	return render_template('/c_viewFlight.html',username=email)

@app.route('/c_futureFlight')
def c_futureFlight():
	email = session['email']
	# cursor used to send queries
	cursor = conn.cursor()
	# executes query
	query = 'SELECT `tkt_id`, al_name, flt_num, dep_dnt, dep_apt, A.city as dep, arr_dnt, arr_apt, B.city as arr, stts FROM ticket NATURAL JOIN purchase NATURAL JOIN flight, airport A, airport B WHERE dep_apt = A.apt_name and arr_apt = B.apt_name and dep_dnt >= now() and email = %s  '
	cursor.execute(query, (email))
	data = cursor.fetchall()
	cursor.close()

	return render_template('c_futureflight.html', username=email, posts=data)

@app.route('/c_pastFlight')
def c_pastFlight():
	email = session['email']
	# cursor used to send queries
	cursor = conn.cursor()
	# executes query
	query = 'SELECT tkt_id, al_name, ap_id, flt_num, dep_dnt, dep_apt, A.city as dep, arr_dnt, arr_apt, B.city as arr, stts FROM ticket NATURAL JOIN purchase NATURAL JOIN flight, airport A, airport B WHERE dep_apt = A.apt_name and arr_apt = B.apt_name and dep_dnt < now() and email = %s  '
	cursor.execute(query, (email))
	data = cursor.fetchall()
	cursor.close()


	return render_template('c_pastFlight.html', username=email, posts=data)

@app.route('/c_searchFlight')
def c_searchFlight():
	return render_template('/c_searchFlight.html')

@app.route('/c_searchFlightAuth',methods=['GET', 'POST'])
def c_searchFlightAuth():
	email=session['email']
	dep_airport = request.form['s_airport']
	arr_airport = request.form['d_airport']
	d_date = request.form['d_date']
	r_date = request.form['r_date']

	# Search for Airports or City
	# Search for Round or not
	x = request.form.get("is_airport")  # None 说明search for city / On 说明 search for airport
	y = request.form.get("is_round") # None 说明 不是round  / On 说明 round (需要填写r_date)
	print(x)
	print(y)
	print(d_date)

	if (d_date == ""):
		error = "Please enter departure date"
		return render_template('/c_searchFlight.html', error = error)

	if (y != None and  r_date == ""):
		error = "Please enter return date"
		return render_template('/c_searchFlight.html', error = error)

	if (x == None):   #city
		cursor = conn.cursor()
		# executes query
		query = 'SELECT al_name, ap_id, flt_num, dep_dnt, A.apt_name dep_apt, A.city as dep_city, arr_dnt, B.apt_name arr_apt, B.city as arr_city, stts FROM flight, airport A, airport B WHERE A.apt_name = flight.dep_apt and B.apt_name = flight.arr_apt and A.city = %s and B.city = %s  and date(dep_dnt) = %s '
		cursor.execute(query, (dep_airport, arr_airport, d_date))
		data = cursor.fetchall()
		if (y != None):
			query2 = 'SELECT al_name, ap_id, flt_num, dep_dnt, A.apt_name dep_apt, A.city as dep_city, arr_dnt, B.apt_name arr_apt, B.city as arr_city, stts FROM flight, airport A, airport B WHERE A.apt_name = flight.dep_apt and B.apt_name = flight.arr_apt and A.city = %s and B.city = %s  and date(dep_dnt) = %s '
			cursor.execute(query2, (arr_airport, dep_airport, r_date))
			data += cursor.fetchall()
	
	elif (x != None):  # airport
		cursor = conn.cursor()
		# executes query
		query = 'SELECT al_name, ap_id, flt_num, dep_dnt, A.apt_name dep_apt, A.city as dep_city, arr_dnt, B.apt_name arr_apt, B.city as arr_city, stts FROM flight, airport A, airport B WHERE A.apt_name = flight.dep_apt and B.apt_name = flight.arr_apt and A.apt_name = %s and B.apt_name = %s  and date(dep_dnt) = %s'
		cursor.execute(query, (dep_airport, arr_airport, d_date))
		data = cursor.fetchall()
		if (y != None):
			query2 = 'SELECT al_name, ap_id, flt_num, dep_dnt, A.apt_name dep_apt, A.city as dep_city, arr_dnt, B.apt_name arr_apt, B.city as arr_city, stts FROM flight, airport A, airport B WHERE A.apt_name = flight.dep_apt and B.apt_name = flight.arr_apt and A.apt_name = %s and B.apt_name = %s  and date(dep_dnt) = %s'
			cursor.execute(query2, (arr_airport, dep_airport, r_date))
			data += cursor.fetchall()



	if(data):
		return render_template('c_searchFlight.html', posts=data)
	else:
		return render_template('c_searchFlight.html', error='Sorry, no such flight exist.')

@app.route('/c_purchase', methods=['GET', 'POST'])
def c_purchase():
	email = session['email']
	al_name = request.form["al_name"]
	ap_id = request.form["ap_id"]
	flt_num = request.form['flt_num']
	dep_dnt = request.form['dep_dnt']
	print(al_name, ap_id, flt_num, dep_dnt )

	cursor = conn.cursor()
	# executes query
	query = 'SELECT base_price, seat_num FROM flight NATURAL JOIN airplane WHERE flt_num = %s AND dep_dnt = %s '
	cursor.execute(query, (flt_num, dep_dnt))
	data = cursor.fetchone()
	price=float(data['base_price'])
	seat=int(data['seat_num'])

	query2 = 'SELECT COUNT(tkt_id) AS sold_num FROM ticket WHERE flt_num = %s AND dep_dnt = %s and al_name = %s and ap_id = %s'
	cursor.execute(query2, (flt_num, dep_dnt, al_name, ap_id ))
	data1 = cursor.fetchone()
	sold=data1['sold_num']

	cursor.close()

	if (sold==seat):
		return render_template('c_searchFlight.html', error2='Sorry, no more tickets available.')
	elif (sold/seat >= 0.6):
		# print(6666666666666666)
		price=price*1.2
		seat=seat-sold
		return render_template('c_purchase.html', username=email, al_name = al_name, flt_num=flt_num, ap_id = ap_id, dep_dnt=dep_dnt, price=price, seat=seat)
	else:
		seat=seat-sold
		return render_template('c_purchase.html', username=email, al_name = al_name ,flt_num=flt_num, ap_id = ap_id, dep_dnt=dep_dnt, price=price, seat=seat)

@app.route('/purchaseAuth', methods=['GET', 'POST'])
def purchase_auth():
	print(request.form)
	email = session['email']
	flt_num = request.form['flt_num']
	dep_dnt = request.form['dep_dnt']
	al_name = request.form['al_name']
	ap_id = request.form['ap_id']
	sold_price = request.form['sold_price']
	card_type = request.form['card_type']
	card_num = request.form['card_num']
	card_name = request.form['card_name']
	exp_date = request.form['exp_date']

	cursor = conn.cursor()
	query0 = 'SELECT al_name, dep_dnt FROM flight WHERE flt_num =%s and date(dep_dnt) = %s and ap_id = %s and al_name LIKE %s'
	al_name = '%' + al_name + '%' 
	print(flt_num, dep_dnt, ap_id, al_name)
	cursor.execute(query0, (flt_num, dep_dnt, ap_id, al_name))
	data = cursor.fetchone()
	cursor.close()
	al_name = data["al_name"]
	dep_dnt = data['dep_dnt']
	print(al_name)

	# cursor used to send queries
	cursor = conn.cursor()
	query = 'SELECT MAX(tkt_id) AS max_id FROM ticket'
	cursor.execute(query)
	data = cursor.fetchone()
	id = data['max_id']+1

	ins = 'INSERT INTO ticket VALUES(%s, %s, %s, %s, %s, %s)'
	print(al_name, ap_id, id, flt_num, dep_dnt, sold_price)
	cursor.execute(ins,(al_name, ap_id, id, flt_num, dep_dnt, sold_price))
	conn.commit()

	ins1 = 'INSERT INTO purchase VALUES(%s, %s, now(), %s, %s, %s, %s)'
	cursor.execute(ins1, (id, email, card_type, card_num, card_name, exp_date))
	conn.commit()

	cursor.close()
	return render_template('c_paySuccess.html', username=email)
	
@app.route('/c_trackSpending', methods=['GET', 'POST'])
def c_trackSpending():
	email = session['email']
	cursor = conn.cursor()
	query = 'SELECT sum(sold_price) as sum FROM purchase NATURAL JOIN ticket WHERE email = %s and DATE_SUB(now(), INTERVAL 6 MONTH) <= purch_dnt'
	cursor.execute(query, (email))
	data = cursor.fetchone()
	cursor.close()
	print(data['sum'])
	spend = data['sum']
	
	cursor = conn.cursor()
	query = 'SELECT purch_dnt as date, sold_price as total FROM purchase NATURAL JOIN ticket WHERE email = %s and DATE_SUB(now(), INTERVAL 6 MONTH) <= purch_dnt order by purch_dnt '
	cursor.execute(query, (email))
	data2 = cursor.fetchall()
	cursor.close()

	return render_template('/c_trackSpending.html', email = email, spend = spend, posts2 = data2)

@app.route('/trackSpending_auth',methods=['GET', 'POST'])
def trackSpending_auth():
	email = session['email']
	start_date = request.form['start_date']
	end_date = request.form['end_date']
	print(email,start_date, end_date)

	cursor = conn.cursor()
	query = 'SELECT sum(sold_price) as sum FROM purchase NATURAL JOIN ticket WHERE email = %s and purch_dnt BETWEEN %s AND %s'
	cursor.execute(query, (email, start_date, end_date))
	data = cursor.fetchone()
	cursor.close()
	print(data['sum'])
	spend = data['sum']
	
	cursor = conn.cursor()
	query = 'SELECT purch_dnt as date, sold_price as total FROM purchase NATURAL JOIN ticket WHERE email = %s and purch_dnt BETWEEN %s AND %s order by purch_dnt '
	cursor.execute(query, (email, start_date, end_date))
	data2 = cursor.fetchall()
	cursor.close()


	return render_template('/c_mySpend.html', email = email, spend = spend, posts2 = data2, start_date = start_date, end_date = end_date)


@app.route('/c_cancel')
def c_cancel():
	
	return render_template('c_cancel.html')

@app.route('/c_cancel_auth', methods=['GET', 'POST'])
def c_cancel_auth():

	email = session['email']
	ticketNum = request.form['ticketID']
	print(email)
	print(ticketNum)
	# cursor used to send queries
	cursor = conn.cursor()
	# executes query
	query = 'SELECT tkt_id, al_name, flt_num, dep_dnt, dep_apt, A.city as dep, arr_dnt, arr_apt, B.city as arr, stts FROM ticket NATURAL JOIN purchase NATURAL JOIN flight, airport A, airport B WHERE dep_apt = A.apt_name and arr_apt = B.apt_name and SUBTIME(now(),"-1:0:0" ) < dep_dnt and tkt_id = %s and email = %s'
	cursor.execute(query, (ticketNum,email))
	data = cursor.fetchone()
	# message = "Cancelation failed"
	message = None
	if(data):
		query2 = 'DELETE FROM purchase WHERE tkt_id = %s and email = %s '
		cursor.execute(query2, (ticketNum,email))
		conn.commit()
		cursor.close()
		message = "Cancelation success"
		return render_template('c_cancel.html', message=message)
	else:
		cursor.close()
		#returns an error message to the html page
		message = "Cancelation failed"
		return render_template('c_cancel.html', message=message)


@app.route('/c_rate', methods=['GET', 'POST'])
def c_rate():
	email = session['email']
	# al_name = request.form["al_name"]
	flt_num = request.form['flt_num']
	dep_dnt = request.form['dep_dnt']
	ap_id = request.form['ap_id']
	# print(al_name)
	al_name = request.form.get("al_name")
	cursor = conn.cursor()
	query = 'SELECT al_name FROM ticket NATURAL JOIN purchase NATURAL JOIN flight WHERE dep_dnt < now() and email = %s and flt_num =%s and dep_dnt = %s and ap_id = %s'
	cursor.execute(query, (email, flt_num, dep_dnt, ap_id))
	data = cursor.fetchone()
	cursor.close()
	al_name = data["al_name"]
	print(al_name,ap_id)
	# print(data["al_name"])
	# print(flt_num)
	# print(dep_dnt)
	# print(email)
	# print(77777777777777777777777777777777)
	return render_template('c_rate.html', username=email, al_name = al_name, ap_id = ap_id, flt_num=flt_num, dep_dnt=dep_dnt)


@app.route('/c_rateFlight', methods=['GET', 'POST'])
def c_rateFlight():
	email = session['email']
	# al_name = request.form["al_name"]
	flt_num = request.form['flt_num']
	dep_dnt = request.form['dep_dnt']
	ap_id = request.form['ap_id']
	rate = request.form['rate']
	comment = request.form['comment']
	cursor = conn.cursor()
	query = 'SELECT al_name FROM ticket NATURAL JOIN purchase NATURAL JOIN flight WHERE dep_dnt < now() and email = %s and flt_num =%s and dep_dnt = %s and ap_id = %s'
	cursor.execute(query, (email, flt_num, dep_dnt, ap_id))
	data = cursor.fetchone()
	cursor.close()
	al_name = data["al_name"]

	# cursor used to send queries
	cursor = conn.cursor()
	# executes query
	query = 'SELECT * FROM rate WHERE email = %s AND flt_num = %s AND dep_dnt = %s AND al_name = %s and ap_id =%s'
	cursor.execute(query, (email, flt_num, dep_dnt, al_name, ap_id))
	# stores the results in a variable
	data = cursor.fetchone()
	error = None
	if (data):
		# If the previous query returns data, then user exists
		error = "You have already rated/commented this flight"
		return render_template('c_rate.html', username=email, al_name = al_name, ap_id = ap_id, flt_num=flt_num, dep_dnt=dep_dnt, error = error)
	else:
		ins = 'INSERT INTO rate VALUES(%s, %s, %s, %s, %s, %s, %s)'
		# print(al_name,flt_num,dep_dnt,email )
		cursor.execute(ins,(al_name, ap_id, flt_num, dep_dnt, email, rate, comment))
		conn.commit()
		cursor.close()
		# error = "Thank you for comment"
		return redirect(url_for('c_pastFlight'))
		

# Customer logout
@app.route('/c_logout')
def c_logout():
	session.pop('email')
	return redirect('/')


@app.route('/g_search')
def g_search():
	return render_template("g_search.html")

@app.route('/g_searchFlightAuth',methods=['GET', 'POST'])
def g_searchFlightAuth():
	dep_airport = request.form['s_airport']
	arr_airport = request.form['d_airport']
	d_date = request.form['d_date']
	r_date = request.form['r_date']

	# Search for Airports or City
	# Search for Round or not
	x = request.form.get("is_airport")  # None 说明search for city / On 说明 search for airport
	y = request.form.get("is_round") # None 说明 不是round  / On 说明 round (需要填写r_date)
	print(x)
	print(y)
	print(d_date)

	if (d_date == ""):
		error = "Please enter departure date"
		return render_template('/g_search.html', error = error)

	if (y != None and  r_date == ""):
		error = "Please enter return date"
		return render_template('/g_search.html', error = error)

	if (x == None):   #city
		cursor = conn.cursor()
		# executes query
		query = 'SELECT al_name, ap_id, flt_num, dep_dnt, A.apt_name dep_apt, A.city as dep_city, arr_dnt, B.apt_name arr_apt, B.city as arr_city, stts FROM flight, airport A, airport B WHERE A.apt_name = flight.dep_apt and B.apt_name = flight.arr_apt and A.city = %s and B.city = %s  and date(dep_dnt) = %s '
		cursor.execute(query, (dep_airport, arr_airport, d_date))
		data = cursor.fetchall()
		if (y != None):
			query2 = 'SELECT al_name, ap_id, flt_num, dep_dnt, A.apt_name dep_apt, A.city as dep_city, arr_dnt, B.apt_name arr_apt, B.city as arr_city, stts FROM flight, airport A, airport B WHERE A.apt_name = flight.dep_apt and B.apt_name = flight.arr_apt and A.city = %s and B.city = %s  and date(dep_dnt) = %s '
			cursor.execute(query2, (arr_airport, dep_airport, r_date))
			data += cursor.fetchall()
	
	elif (x != None):  # airport
		cursor = conn.cursor()
		# executes query
		query = 'SELECT al_name, ap_id, flt_num, dep_dnt, A.apt_name dep_apt, A.city as dep_city, arr_dnt, B.apt_name arr_apt, B.city as arr_city, stts FROM flight, airport A, airport B WHERE A.apt_name = flight.dep_apt and B.apt_name = flight.arr_apt and A.apt_name = %s and B.apt_name = %s  and date(dep_dnt) = %s'
		cursor.execute(query, (dep_airport, arr_airport, d_date))
		data = cursor.fetchall()
		if (y != None):
			query2 = 'SELECT al_name, ap_id, flt_num, dep_dnt, A.apt_name dep_apt, A.city as dep_city, arr_dnt, B.apt_name arr_apt, B.city as arr_city, stts FROM flight, airport A, airport B WHERE A.apt_name = flight.dep_apt and B.apt_name = flight.arr_apt and A.apt_name = %s and B.apt_name = %s  and date(dep_dnt) = %s'
			cursor.execute(query2, (arr_airport, dep_airport, r_date))
			data += cursor.fetchall()

	if(data):
		return render_template('g_search.html', posts=data)
	else:
		return render_template('g_search.html', error='Sorry, no such flight exist.')


@app.route('/check_status')
def check_status():

	return render_template('g_status.html')

@app.route('/check_status_auth',methods=['GET', 'POST'])
def check_status_auth():
	x = request.form.get("arr_apt")  # None 说明search dep / On 说明 search for arr

	al_name = request.form['al_name']
	flt_num = request.form['flt_num']
	d_date = request.form['d_date']

	if (x == None):
		cursor = conn.cursor()
		query = 'SELECT al_name, flt_num, dep_dnt, arr_dnt, stts FROM flight WHERE al_name =%s and flt_num = %s and date(dep_dnt) = %s'
		cursor.execute(query, (al_name, flt_num, d_date))
		data = cursor.fetchall()
		cursor.close()
	else:
		cursor = conn.cursor()
		query = 'SELECT al_name, flt_num, dep_dnt, arr_dnt, stts FROM flight WHERE al_name =%s and flt_num = %s and date(arr_dnt) = %s'
		cursor.execute(query, (al_name, flt_num, d_date))
		data = cursor.fetchall()
		cursor.close()

	if (data):
		error = ''
		return render_template('g_status.html', posts = data, error = error)
	else:
		print(666666)
		error = "Sorry, no such flight exist" 
		return render_template('g_status.html', posts = data, error = error)




# Define a route to the staff register page 
@app.route('/s_register')
def s_register():
	return render_template('s_register.html')

# Define a route to the staff login page 
@app.route('/s_login')
def s_login():
	return render_template('s_login.html')

# Authenticates staff register
@app.route('/s_register_auth', methods=['GET', 'POST'])
def s_register_auth():
	# grabs information from the forms
	us_name = request.form['us_name']
	al_name = request.form['al_name']
	pswd = request.form['pswd']
	f_name = request.form['f_name']
	l_name = request.form['l_name']
	dob = request.form['dob']

	print(us_name, al_name, pswd, f_name, l_name, dob)

	# cursor used to send queries
	cursor = conn.cursor()
	# executes query
	query = 'SELECT * FROM staff WHERE us_name = %s'
	cursor.execute(query, (us_name))
	# stores the results in a variable
	data = cursor.fetchone()
	# use fetchall() if you are expecting more than 1 data row
	error = None
	if (data):
		# If the previous query returns data, then user exists
		error = "This user already exists"
		return render_template('s_register.html', error=error)
	else:
		ins = 'INSERT INTO staff VALUES(%s, %s, MD5(%s), %s, %s, %s)'
		cursor.execute(ins, (us_name, al_name, pswd, f_name, l_name, dob))
		conn.commit()
		cursor.close()
		return render_template('s_login.html')

# Authenticates the staff login
@app.route('/s_login_auth', methods=['GET', 'POST'])
def s_login_auth():
	# grabs information from the forms
	us_name = request.form['us_name']
	pswd = request.form['pswd']

	# cursor used to send queries
	cursor = conn.cursor()
	# executes query
	query = 'SELECT * FROM staff WHERE us_name = %s and pswd = MD5(%s)'
	cursor.execute(query, (us_name, pswd))
	# stores the results in a variable
	data = cursor.fetchone()
	# use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None
	if (data):
		# creates a session for the the user
		# session is a built in
		# cursor used to send queries
		cursor = conn.cursor()
		# executes query
		query = 'SELECT al_name FROM staff WHERE us_name = %s'
		cursor.execute(query, (us_name))
		# stores the results in a variable
		data = cursor.fetchone()
		# use fetchall() if you are expecting more than 1 data row
		cursor.close()
		al_name = data['al_name']
		session['us_name'] = us_name
		session['al_name'] = al_name

		return redirect(url_for('s_homepage'))
	else:
		# returns an error message to the html page
		error = 'Invalid login or username'
		return render_template('s_login.html', error=error)

# Staff home page
@app.route('/s_homepage')
def s_homepage():
	us_name = session['us_name']
	al_name = session['al_name']
	return render_template('s_homepage.html', us_name=us_name, al_name=al_name)

@app.route('/s_logout')
def logout():
	session.pop('us_name')
	return redirect('/')

@app.route('/s_flightInfo')
def s_flightInfo():
	us_name = session['us_name']
	al_name = session['al_name']

	cursor = conn.cursor()
	query = 'SELECT ap_id, flt_num, dep_dnt, dep_apt, arr_apt, arr_dnt, base_price, stts FROM flight WHERE al_name = %s AND dep_dnt > CURRENT_TIMESTAMP AND dep_dnt < CURRENT_TIMESTAMP + INTERVAL 1 MONTH'
	cursor.execute(query, (al_name))
	data = cursor.fetchall()
	cursor.close()

	if (data):
		return render_template('s_flightInfo.html', us_name=us_name, al_name=al_name, posts=data)
	else:
		return render_template('s_flightInfo.html', us_name=us_name, al_name=al_name)

@app.route('/s_addFlight', methods=['GET', 'POST'])
def s_addFlight():
	# grabs information from the forms
	us_name = session['us_name']
	al_name = session['al_name']
	ap_id = request.form['ap_id']
	flt_num = request.form['flt_num']
	dep_dnt = request.form['dep_dnt']
	dep_apt = request.form['dep_apt']
	arr_dnt = request.form['arr_dnt']
	arr_apt = request.form['arr_apt']
	base_price = request.form['base_price']
	stts = request.form['stts']

	# cursor used to send queries
	cursor = conn.cursor()
	# executes query
	query = 'SELECT * FROM flight WHERE flt_num = %s and dep_dnt = %s'
	cursor.execute(query, (flt_num, dep_dnt))
	# stores the results in a variable
	data = cursor.fetchone()
	# use fetchall() if you are expecting more than 1 data row
	query1 = 'SELECT ap_id, flt_num, dep_dnt, dep_apt, arr_dnt, arr_apt, base_price, stts FROM flight WHERE al_name = %s AND dep_dnt > CURRENT_TIMESTAMP AND dep_dnt < CURRENT_TIMESTAMP + INTERVAL 1 MONTH'
	cursor.execute(query1, (al_name))
	data1 = cursor.fetchall()
	cursor.close()
	error = None
	if (data):
		# If the previous query returns data, then user exists
		error = "This flight already exists"
		return render_template('s_flightInfo.html', us_name=us_name, al_name=al_name, posts=data1, error=error)
	else:
		cursor = conn.cursor()
		ins = 'INSERT INTO flight VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)'
		cursor.execute(ins, (al_name, ap_id, flt_num, dep_dnt, dep_apt, arr_dnt, arr_apt, base_price, stts))
		conn.commit()
		cursor.close()
		return redirect(url_for('s_flightInfo'))

@app.route('/s_changeStatus', methods=['GET', 'POST'])
def s_changeStatus():
	flt_num = request.form['flt_num']
	dep_dnt = request.form['dep_dnt']
	stts = request.form['stts']
	cursor = conn.cursor()
	if(stts=="on-time"):
		update = 'Update flight SET stts = "delayed" WHERE flt_num = %s and dep_dnt = %s'
		cursor.execute(update, (flt_num, dep_dnt))
	else:
		update = 'Update flight SET stts = "on-time" WHERE flt_num = %s and dep_dnt = %s'
		cursor.execute(update, (flt_num, dep_dnt))
	conn.commit()
	cursor.close()
	return redirect("/s_flightInfo")

@app.route('/s_changeStatus_sf', methods=['GET', 'POST'])
def s_changeStatus_sf():
	flt_num = request.form['flt_num']
	dep_dnt = request.form['dep_dnt']
	stts = request.form['stts']
	cursor = conn.cursor()
	if(stts=="on-time"):
		update = 'Update flight SET stts = "delayed" WHERE flt_num = %s and dep_dnt = %s'
		cursor.execute(update, (flt_num, dep_dnt))
	else:
		update = 'Update flight SET stts = "on-time" WHERE flt_num = %s and dep_dnt = %s'
		cursor.execute(update, (flt_num, dep_dnt))
	conn.commit()
	cursor.close()
	return redirect("/s_searchFlight")

@app.route('/s_viewRate', methods=['GET', 'POST'])
def s_viewRate():
	us_name = session['us_name']
	al_name = session['al_name']
	flt_num = request.form['flt_num']
	dep_dnt = request.form['dep_dnt']
	cursor = conn.cursor()
	query = 'SELECT email, rate, com FROM rate WHERE flt_num = %s and dep_dnt = %s ORDER BY email DESC'
	cursor.execute(query, (flt_num, dep_dnt))
	data = cursor.fetchall()
	query2 = 'SELECT avg(rate) as avg_rate From rate WHERE flt_num = %s and dep_dnt = %s'
	cursor.execute(query2, (flt_num, dep_dnt))
	data1 = cursor.fetchone()
	cursor.close()
	if (data):
		return render_template('s_viewRate.html', al_name=al_name, flt_num=flt_num, dep_dnt=dep_dnt, posts=data, avg_rate=data1)
	else:
		return render_template('s_viewRate.html', al_name=al_name, flt_num=flt_num, dep_dnt=dep_dnt, error="No Ratings Yet")
		
@app.route('/s_viewRate_sf', methods=['GET', 'POST'])
def s_viewRate_sf():
	us_name = session['us_name']
	al_name = session['al_name']
	flt_num = request.form['flt_num']
	dep_dnt = request.form['dep_dnt']
	cursor = conn.cursor()
	query = 'SELECT email, rate, com FROM rate WHERE flt_num = %s and dep_dnt = %s ORDER BY email DESC'
	cursor.execute(query, (flt_num, dep_dnt))
	data = cursor.fetchall()
	query2 = 'SELECT avg(rate) as avg_rate From rate WHERE flt_num = %s and dep_dnt = %s'
	cursor.execute(query2, (flt_num, dep_dnt))
	data1 = cursor.fetchone()
	cursor.close()
	if (data):
		return render_template('s_viewRate_sf.html', al_name=al_name, flt_num=flt_num, dep_dnt=dep_dnt, posts=data, avg_rate=data1)
	else:
		return render_template('s_viewRate_sf.html', al_name=al_name, flt_num=flt_num, dep_dnt=dep_dnt, error="No Ratings Yet")
			
@app.route('/s_searchFlight')
def s_searchFlight():
	us_name = session['us_name']
	al_name = session['al_name']
	return render_template('s_searchFlight.html', us_name=us_name, al_name=al_name)

@app.route('/s_flightSearch', methods=['GET', 'POST'])
def s_flightSearch():
#grabs information from the forms
	us_name=session['us_name']
	al_name=session['al_name']
	s_airport = request.form['s_airport']
	d_airport = request.form['d_airport']
	s_date = request.form['s_date']
	e_date = request.form['e_date']

	#find if it is an airport search or a location search
	if request.form.get("is_airport"):
		is_airport = request.form['is_airport']
	else:
		is_airport = 'off'


	if(is_airport=='on'):
		#cursor used to send queries
		cursor = conn.cursor()
		#executes query
		query = 'SELECT ap_id, flt_num, dep_dnt, dep_apt, arr_dnt, arr_apt, base_price, stts FROM flight JOIN airport S JOIN airport D WHERE S.apt_name = flight.dep_apt and D.apt_name = flight.arr_apt AND al_name = %s AND S.apt_name = %s AND D.apt_name = %s'
		cursor.execute(query, (al_name, s_airport, d_airport))
		data = cursor.fetchall()
	elif(is_airport=='off' and s_airport!=''):
		cursor = conn.cursor()
		# executes query
		query = 'SELECT ap_id, flt_num, dep_dnt, dep_apt, arr_dnt, arr_apt, base_price, stts FROM flight JOIN airport S JOIN airport D WHERE S.apt_name = flight.dep_apt and D.apt_name = flight.arr_apt AND al_name = %s AND S.city = %s AND D.city = %s'
		cursor.execute(query, (al_name, s_airport, d_airport))
		data = cursor.fetchall()
	else:
		cursor = conn.cursor()
		# executes query
		query = 'SELECT ap_id, flt_num, dep_dnt, dep_apt, arr_dnt, arr_apt, base_price, stts FROM flight WHERE al_name = %s AND dep_dnt > %s AND dep_dnt < %s'
		cursor.execute(query, (al_name, s_date, e_date))
		data = cursor.fetchall()

	cursor.close()

	if(data):
		return render_template('s_searchFlight.html', posts=data)
	else:
		return render_template('s_searchFlight.html', error='Sorry, no such flight exist.')

@app.route('/s_viewCustomer', methods=['GET', 'POST'])
def s_viewCustomer():
	flt_num = request.form['flt_num']
	dep_dnt = request.form['dep_dnt']
	cursor = conn.cursor()
	query = 'SELECT email, tkt_id, purch_dnt FROM purchase NATURAL JOIN ticket NATURAL JOIN flight WHERE flt_num= %s AND dep_dnt= %s'
	cursor.execute(query, (flt_num, dep_dnt))
	data = cursor.fetchall()
	cursor.close()
	if(data):
		return render_template('s_viewCustomer.html', posts=data, flt_num=flt_num, dep_dnt=dep_dnt)
	else:
		return render_template('s_viewCustomer.html', posts=data, flt_num=flt_num, error='No customers yet!')

@app.route('/s_viewRevenue')
def s_viewRevenue():
	al_name = session['al_name']
	cursor = conn.cursor()
	query = 'SELECT SUM(sold_price) AS month_total, MONTH(purch_dnt) month FROM purchase NATURAL JOIN ticket NATURAL JOIN flight WHERE MONTH(purch_dnt) = MONTH(CURRENT_DATE) AND YEAR(purch_dnt) = YEAR(CURRENT_DATE) AND al_name = %s GROUP BY MONTH(purch_dnt)'
	cursor.execute(query, (al_name))
	data = cursor.fetchone()
	month_total=data['month_total']
	month=data['month']
	query2 = 'SELECT SUM(sold_price) AS year_total, YEAR(purch_dnt) year FROM purchase NATURAL JOIN ticket NATURAL JOIN flight WHERE YEAR(purch_dnt) = YEAR(CURRENT_DATE) AND al_name = %s GROUP BY YEAR(purch_dnt)'
	cursor.execute(query2, (al_name))
	data1 = cursor.fetchone()
	year_total = data1['year_total']
	year = data1['year']
	cursor.close()
	return render_template('s_viewRevenue.html', month=month, month_total=month_total, year=year, year_total=year_total)

@app.route('/s_modiApAp')
def s_modiApAp():
	al_name = session['al_name']
	cursor = conn.cursor()
	query = 'SELECT ap_id, seat_num, company, age FROM airplane WHERE al_name = %s ORDER BY ap_id DESC'
	cursor.execute(query, (al_name))
	data = cursor.fetchall()

	if (data):
		return render_template('s_modiApAp.html', al_name=al_name, posts=data)
	else:
		return render_template('s_modiApAp.html', al_name=al_name)

@app.route('/s_addAirplane', methods=['GET', 'POST'])
def s_addAirplane():
	# grabs information from the forms
	ap_id = request.form['ap_id']
	al_name = session['al_name']
	seat_num = request.form['seat_num']
	company = request.form['company']
	age = request.form['age']

	# cursor used to send queries
	cursor = conn.cursor()
	# executes query
	query = 'SELECT * FROM airplane WHERE al_name = %s and ap_id = %s'
	cursor.execute(query, (al_name, ap_id))
	# stores the results in a variable
	data = cursor.fetchone()
	# use fetchall() if you are expecting more than 1 data row
	error = None
	if (data):
		# If the previous query returns data, then user exists
		cursor = conn.cursor()
		query = 'SELECT ap_id, seat_num FROM airplane WHERE al_name = %s ORDER BY ap_id DESC'
		cursor.execute(query, (al_name))
		data1 = cursor.fetchall()
		error = "This plane already exists"
		return render_template('/s_modiApAp.html', al_name=al_name, posts=data1, error=error)
	else:
		ins = 'INSERT INTO airplane VALUES(%s, %s, %s, %s, %s)'
		cursor.execute(ins, (ap_id, al_name, seat_num, company, age))
		conn.commit()
		cursor.close()
		return redirect("/s_modiApAp")

@app.route('/s_addAirport', methods=['GET', 'POST'])
def s_addAirport():
	# grabs information from the forms
	al_name=session['al_name']
	apt_name = request.form['apt_name']
	city = request.form['city']
	country = request.form['country']
	apt_type = request.form['apt_type']

	# cursor used to send queries
	cursor = conn.cursor()
	# executes query
	query = 'SELECT * FROM airport WHERE apt_name = %s'
	cursor.execute(query, (apt_name))
	# stores the results in a variable
	data = cursor.fetchone()
	print(data)
	# use fetchall() if you are expecting more than 1 data row
	error = None
	if (data):
		# If the previous query returns data, then user exists
		query = 'SELECT ap_id, seat_num FROM airplane WHERE al_name = %s ORDER BY ap_id DESC'
		cursor.execute(query, (al_name))
		data1 = cursor.fetchall()
		cursor.close()
		error1 = "This airport already exists"
		return render_template('as_modiApAp.html', al_name=al_name, posts=data1, error1=error1)
	else:
		ins = 'INSERT INTO airport VALUES(%s, %s, %s, %s)'
		cursor.execute(ins, (apt_name, city, country, apt_type))
		conn.commit()
		cursor.close()
		return redirect("/s_modiApAp")

@app.route('/s_viewStat')
def s_viewStat():
	al_name = session['al_name']
	cursor = conn.cursor()
	query = 'SELECT email, COUNT(tkt_id) FROM purchase NATURAL JOIN ticket NATURAL JOIN flight WHERE al_name = %s GROUP BY email ORDER BY email DESC'
	cursor.execute(query, (al_name))
	data = cursor.fetchone()
	email = data['email']
	query1 = 'SELECT flt_num, dep_dnt, dep_apt, arr_dnt, arr_apt, tkt_id FROM purchase NATURAL JOIN ticket NATURAL JOIN flight WHERE email = %s AND al_name= %s'
	cursor.execute(query1, (email, al_name))
	data1 = cursor.fetchall()

	cursor.close()

	return render_template('s_viewStat.html', al_name=al_name, top_c=email, posts=data1)

@app.route('/s_ticketSold', methods=['GET', 'POST'])
def s_ticketSold():
	al_name = session['al_name']
	if request.form.get("s_date"):
		s_date = request.form['s_date']
		e_date = request.form['e_date']
	else:
		s_date = 'off'
	if request.form.get("is_year"):
		is_year = request.form['is_year']
	else:
		is_year = 'off'
	if request.form.get("is_month"):
		is_month = request.form['is_month']
	else:
		is_month = 'off'

	if (s_date != 'off' ):
		cursor = conn.cursor()
		query = 'SELECT COUNT(tkt_id) AS tkt_total, MONTH(purch_dnt) month FROM purchase NATURAL JOIN ticket NATURAL JOIN flight WHERE purch_dnt > %s AND purch_dnt < %s AND al_name = %s GROUP BY MONTH(purch_dnt) ORDER BY month DESC'
		cursor.execute(query, (s_date, e_date, al_name))
		data = cursor.fetchall()
		return render_template('s_ticketSold.html', posts=data, s_date=s_date, e_date=e_date)
	elif (is_month == 'on'):
		cursor = conn.cursor()
		query = 'SELECT COUNT(tkt_id) AS tkt_total, MONTH(purch_dnt) month FROM purchase NATURAL JOIN ticket NATURAL JOIN flight WHERE purch_dnt > CURRENT_DATE - INTERVAL 1 MONTH AND purch_dnt < CURRENT_DATE AND al_name = %s GROUP BY MONTH(purch_dnt) ORDER BY month DESC'
		cursor.execute(query, (al_name))
		data = cursor.fetchall()
		return render_template('s_ticketSold.html', posts=data, is_month=is_month)
	else:
		cursor = conn.cursor()
		query = 'SELECT COUNT(tkt_id) AS tkt_total, MONTH(purch_dnt) month FROM purchase NATURAL JOIN ticket NATURAL JOIN flight WHERE purch_dnt > CURRENT_DATE - INTERVAL 12 MONTH AND purch_dnt < CURRENT_DATE AND al_name = %s GROUP BY MONTH(purch_dnt) ORDER BY month DESC'
		cursor.execute(query, (al_name))
		data = cursor.fetchall()
		return render_template('s_ticketSold.html', posts=data, is_year=is_year)

app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)
