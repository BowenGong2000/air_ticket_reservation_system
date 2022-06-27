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
		error = "No such flight" 
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


@app.route('/logout')
def logout():
	session.pop('username')
	return redirect('/')


		
app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)
