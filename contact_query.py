from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators
from wtforms.validators import DataRequired, Email, Required
from flask_mail import Mail, Message
import os
app=Flask(__name__)             #takes the name of the place where the app is defined



app.config['SECRET_KEY'] = "vyking0%1@"

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = "webdev.projects.9012@gmail.com"
app.config['MAIL_PASSWORD'] = "Vyking0%1@"
app.config['MAIL_USE_TLS'] = False             #Use for encryption purposes
app.config['MAIL_USE__SSL'] = True

mail=Mail(app)

@app.route('/',methods=['GET','POST'])
def index():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        pno = request.form['pno']
        query = request.form['query']

        message = Message(query, sender = "webdev.projects.9012@gmail.com", recipients = ["simrangarg0501@gmail.com"])

        message.body = name + '\n' + pno + '\n' + query

        mail.send(message)

        flash("Query has been submitted!")

        return redirect(url_for('index'))
    
    return render_template('index.html')
    
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html') , 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html') , 500