from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators
from wtforms.validators import DataRequired, Email, Required
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
import os
basedir=os.path.abspath(os.path.dirname(__file__))
app=Flask(__name__)             #takes the name of the place where the app is defined

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "vyking0%1@"

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = "webdev.projects.9012@gmail.com"
app.config['MAIL_PASSWORD'] = "Vyking0%1@"
app.config['MAIL_USE_TLS'] = True          #Use for encryption purposes

db=SQLAlchemy(app)
mail=Mail(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(30), unique=True, index=True)
    pno = db.Column(db.String(10), unique = True, index=True)
    query_msg = db.Column(db.String(250))

    def __repr__(self):
        return f"User('{self.name}','{self.email}','{self.pno}','{self.query_msg}' )"


@app.route('/',methods=['GET','POST'])
def index():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        pno = request.form['pno']
        query_msg = request.form['query_msg']
        user=User.query.filter_by(email=email).first()
        if user is None:
            user=User(name=name, email=email, pno=pno, query_msg=query_msg )
            db.session.add(user)
            db.session.commit()
            session['exists'] = False
            message = Message("new query", sender = "webdev.projects.9012@gmail.com", recipients = ["webdev.projects.9012@gmail.com"])
            message.body = 'Name: '+ name + '\n' + 'Contact Number: ' + pno + '\n' + 'Email: '+ email + '\n' + 'Query: '+ query_msg
            mail.send(message)
            flash("Thanks for submitting your query!")
        else:
            session['exists'] = True
            flash("Your query has been already submitted!")
        return redirect(url_for('index'))
    return render_template('index.html',exists=session.get('exists',False))
    
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html') , 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html') , 500
    