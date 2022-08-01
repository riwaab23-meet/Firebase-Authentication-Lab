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

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/signup', methods=['GET', 'POST'])
def signup():
   error = ""
   if request.method == 'POST':
       email = request.form['email']
       password = request.form['password']
       try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            return redirect(url_for('home'))
       except:
           error = "Authentication failed"
           return render_template("signup.html")

   else:
       print(f"Didn't get to post. got to: {request.method}")
       return render_template("signup.html")


@app.route('/signin', methods=['GET', 'POST'])
def signin():
   error = ""
   if request.method == 'POST':
       email = request.form['email']
       password = request.form['password']
       try:
               login_session['user'] = auth.sign_in_with_email_and_password(email, password)
               return redirect(url_for('home'))
       except:
           error = "Authentication failed"

   else:
   	print(f"Didn't get to post. got to: {request.method}")
   	return render_template("signin.html")



@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    return render_template("add_tweet.html")


if __name__ == '__main__':
    app.run(debug=True)