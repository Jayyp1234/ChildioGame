import re
from unicodedata import name
from flask import render_template, url_for, flash, redirect, request ,send_from_directory,make_response,session, copy_current_request_context
from childiogame import app, db, socket
from .forms import LoginForm,RegistrationForm,RequestResetForm,ResetPasswordForm
from .models import User,Category,Play,Player
import string, random
from flask_socketio import emit, disconnect
from threading import Lock



base_url = 'http://127.0.0.1:5000/'
i = 0
@app.route("/") 
def home():
    return render_template('index.html',
        title='I CALL ON'
    )
@app.route("/host_game",methods=['POST','GET'])
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
    final_string = base_url+'player/'+''.join(request.args['id'])
    data = Play(play_id=request.args['id'], player_host=request.args['name'])
    data1 = Player(game_id=request.args['id'], username=request.args['name'])
    db.session.add(data)
    db.session.add(data1)
    db.session.commit()
    return render_template(
            'generate.html', 
            title='Generate Links for | I CALL ON',
            name = request.args['name'],
            url_path= final_string,
            url_path1 = request.args['id'],
        )
    
@app.route("/waiting_room/<id>",methods=['POST','GET'])
def waiting_room(id=''):
    data = Player.query.filter_by(game_id= id).all()
    data1 = {}
    for i in data:
        data1[i.id] = i.username
    print(data1)
    if request.method == "POST":
        return data1
    return render_template(
            'waiting.html', 
            title='Waiting Room - Share Links for your friends to join | I CALL ON',
            data = data,
            id = id
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
@app.route("/player/<id>" ,methods=['POST','GET'])
def player(id=''):
    if request.method == "POST":
        name = request.form['name']
        data = Player(game_id=id, username=name)
        db.session.add(data)
        db.session.commit()
        return redirect(url_for('waiting_page', name = name, id = id, **request.args))
    return render_template(
            'player.html', 
            title='Enter Your Name | I CALL ON',
        )

@app.route("/waiting")
def waiting_page(id=''):
    return render_template(
            'waitiner.html', 
            title='Waiting for Host to Start | I CALL ON',
        )

