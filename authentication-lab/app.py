from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config = {

  "apiKey": "AIzaSyAtrsmGHPmquowE93UFsHqjar1yjeKHlTU",
  "authDomain": "meow-6e286.firebaseapp.com",
  "projectId": "meow-6e286",
  "storageBucket": "meow-6e286.appspot.com",
  "messagingSenderId": "625647044114",
  "appId": "1:625647044114:web:b6ef6e1b94f2f532807acb",
  "measurementId": "G-NF7GDK6H92",
  "databaseURL":"https://meow-6e286-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase=pyrebase.initialize_app(config)
auth=firebase.auth()
db = firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/signup', methods=['GET', 'POST'])
def signup():
	error = ""
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		bio = request.form['bio']
		full_name = request.form['full_name']
		username = request.form['username']

		try:
			login_session['user'] = auth.create_user_with_email_and_password(email, password)
			user = {"name": full_name, "username": username , "bio" : bio,"email":email,"password":password}
			db.child("Users").child(login_session['user']['localId']).set(user)

			return redirect(url_for('signin'))
		except:
			error = "Authentication failed"
			return render_template("signup.html")

	else:
		print("Didn't get to post.")
		return render_template("signup.html")


@app.route('/', methods=['GET', 'POST'])
def signin():
	error = ""
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		try:
			login_session['user'] = auth.sign_in_with_email_and_password(email, password)
			return redirect(url_for('add_tweet'))
		except:
			error = "Authentication failed"
			return render_template("signin.html")
	else:
		print(f"Didn't get to post. got to: {request.method}")
		return render_template("add_tweet.html")



@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
	error = ""
	if request.method == 'POST':
		text = request.form['text']
		title = request.form['title']

		try:
			login_session['tweet'] = auth.sign_in_with_email_and_password(email, password)
			user = {"text": text, "title": title , "uid" : login_session['user']['localId']}
			db.child("tweets").push(user)
			return redirect(url_for('home'))
		except:
			error = "Authentication failed"
			return render_template("add_tweet.html")

	else:
		print("Didn't get to post. got to: {request.method}")
		return render_template("add_tweet.html")


@app.route('/all_tweets', methods=['GET', 'POST'])
def tweets():
	tweets = db.child("Tweets").get().val()
	return render_template("signin.html")






if __name__ == '__main__':
	app.run(debug=True)