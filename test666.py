#Import Flask Library
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
	query = 'SELECT `tkt_id`, al_name, flt_num, dep_dnt, dep_apt, A.city as dep, arr_dnt, arr_apt, B.city as arr, stts FROM ticket NATURAL JOIN purchase NATURAL JOIN flight, airport A, airport B WHERE dep_apt = A.apt_name and arr_apt = B.apt_name and dep_dnt > now() and email = %s  '
	cursor.execute(query, (email))
	data = cursor.fetchall()
	cursor.close()

	return render_template('c_futureflight.html', username=email, posts=data)


@app.route('/c_cancel')
def c_cancel():
    
    return render_template('c_cancel.html')

@app.route('/c_cancel_auth', methods=['GET', 'POST'])
def c_cancel_auth():
    message = "x"
    return render_template('c_cancel.html', message = message)


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