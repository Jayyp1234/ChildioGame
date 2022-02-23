from flask import render_template, url_for, flash, redirect, request ,send_from_directory,make_response
from childiogame import app, db
from .forms import LoginForm,RegistrationForm,RequestResetForm,ResetPasswordForm
from .models import User,Category

@app.route("/") 
@app.route("/home")
def home():
    return render_template('index.html')
        
@app.route("/display_item")
def display():
    return render_template('display/index.html')
   



