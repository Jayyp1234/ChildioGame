import re
from unicodedata import name
from flask import render_template, url_for, flash, redirect, request ,send_from_directory,make_response
from childiogame import app, db
from .forms import LoginForm,RegistrationForm,RequestResetForm,ResetPasswordForm
from .models import User,Category
import string, random

base_url = 'http://127.0.0.1:5000/'

@app.route("/") 
def home():
    return render_template('index.html',
        title='I CALL ON'
    )
@app.route("/host_game" ,methods=['POST','GET'])
def host_name():
    # GENERATING RANDOM CHARACTERS
    id = list(''.join((random.choice(string.ascii_uppercase) for x in range(15))) +''.join((random.choice(string.digits) for x in range(15))))
    random.shuffle(id)
    final_string = ''.join(id)
    if request.method == "POST":
        id = request.form['id']
        name = request.form['name']
        return redirect(url_for('generate_link', name = name, id = id, **request.args))
    return render_template('host.html', title='Enter Your Name | I CALL ON', code= final_string)


@app.route("/generate")
def generate_link():
    final_string = base_url+'play/'+''.join(request.args['id'])
    return render_template(
            'generate.html', 
            title='Generate Links for | I CALL ON',
            name = request.args['name'],
            url_path= final_string,
            url_path1 = request.args['id'],
        )
    
@app.route("/waiting_room/<id>")
def waiting_room(id=''):
    return render_template(
            'waiting.html', 
            title='Waiting Room - Share Links for your friends to join | I CALL ON',
        )
   
@app.route("/row_call")
def trigger(id=''):
    return render_template(
            'trigger.html', 
            title='Call your LETTER | I CALL ON',
        )

@app.route("/leaderboard")
def leaderboard(id=''):
    return render_template(
            'leaderboard.html', 
            title='Leaderboard Scores | I CALL ON',
        )

@app.route("/play")
def play(id=''):
    return render_template(
            'play.html', 
            title='Play | I CALL ON',
        )