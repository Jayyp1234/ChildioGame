from unicodedata import category
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from childiogame import db,app
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(120), unique=False, nullable=True, default='user')
    password = db.Column(db.String(250),unique=False, nullable=False)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


    def __repr__(self):
        return f"User('{self.id}','{self.name}','{self.role}')"

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"Categories('{self.id}', '{self.title}')"
        
class Play(db.Model):
    __tablename__ = 'play'
    id = db.Column(db.Integer, primary_key=True)
    play_id = db.Column(db.String(120), unique=True, nullable=False)
    player_host = db.Column(db.String(120), unique=False, nullable=False)
    action = db.Column(db.String(120), unique=False, nullable=True)
    player = db.relationship('Player', backref='player')

    def __repr__(self):
        return f"Play('{self.id}', '{self.play_id}', '{self.player_host}')"
    
class Player(db.Model):
    __tablename__ = 'player'
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.String(120), db.ForeignKey('play.play_id'))
    username =  db.Column(db.String(120), unique=False, nullable=False)
    score = db.Column(db.Integer, unique=False, nullable=True, default = 0)

    def __repr__(self):
        return f"Player('{self.id}', '{self.username}', '{self.score}')"


