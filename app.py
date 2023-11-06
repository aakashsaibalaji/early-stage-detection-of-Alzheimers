from __future__ import division, print_function

from flask import Flask, render_template, request
import joblib
import numpy as np
import sqlite3

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename

app = Flask(__name__)

model = joblib.load('model.sav')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/logon')
def logon():
	return render_template('signup.html')

@app.route('/login')
def login():
	return render_template('signin.html')

@app.route("/signup")
def signup():

    username = request.args.get('user','')
    name = request.args.get('name','')
    email = request.args.get('email','')
    number = request.args.get('mobile','')
    password = request.args.get('password','')
    con = sqlite3.connect('signup.db')
    cur = con.cursor()
    cur.execute("insert into `info` (`user`,`email`, `password`,`mobile`,`name`) VALUES (?, ?, ?, ?, ?)",(username,email,password,number,name))
    con.commit()
    con.close()
    return render_template("signin.html")

@app.route("/signin")
def signin():

    mail1 = request.args.get('user','')
    password1 = request.args.get('password','')
    con = sqlite3.connect('signup.db')
    cur = con.cursor()
    cur.execute("select `user`, `password` from info where `user` = ? AND `password` = ?",(mail1,password1,))
    data = cur.fetchone()

    if data == None:
        return render_template("signin.html")    

    elif mail1 == 'admin' and password1 == 'admin':
        return render_template("index.html")

    elif mail1 == str(data[0]) and password1 == str(data[1]):
        return render_template("index.html")
    else:
        return render_template("signup.html")




@app.route("/index")
def index():
    return render_template('index.html')

@app.route('/predict', methods = ['POST'])
def predict():
    if request.method == 'POST':
        #val1, val2, val3, val4, val5, val6, val7, val8,val9,val10,val11 = float(request.form['1']), float(request.form['2']), float(request.form['3']), float(request.form['4']), float(request.form['5']), float(request.form['6']), float(request.form['7']), float(request.form['8']), float(request.form['9']), float(request.form['10']), float(request.form['11'])
        int_features= [float(x) for x in request.form.values()]
        final4=[np.array(int_features)]
        predict = model.predict(final4)

        if predict == 0:
            output='Based on the HW Feature, the Patient is Affected with Alzheimer Disease Dementia'
        elif predict == 1:
            output='Based on the HW Feature, the Patient is Affected with No Alzheimer Disease Dementia'
        elif predict == 2:
            output='Based on the HW Feature, the Patient is Affected with Uncertain Alzheimer Disease Dementia'
       
       
        
        # print(lr_pm)

    return render_template("result.html", output=output)



@app.route("/notebook")
def notebook():
    return render_template("Notebook.html")


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug = True)
