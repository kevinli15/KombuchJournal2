from datetime import date, datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from kombucha import db, login_manager, app
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    seconds = db.relationship('Second', backref='author', lazy=True)
    

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
        return f"User('{self.username}', '{self.email}', '{self.image_file}'), '{self.id}'"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    identification = db.Column(db.String(10), nullable=False)
    date_posted = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    alertemail= db.Column(db.String(30))
    notes = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
class Second(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.String(20))
    flavoring = db.Column(db.Text)
    rating = db.Column(db.String(10))
    date_posted = db.Column(db.Date)
    end_date = db.Column(db.Date)
    alert= db.Column(db.String(30))
    notes = db.Column(db.Text)
    first = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

