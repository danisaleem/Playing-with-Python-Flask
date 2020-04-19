# from app import app
from datetime import datetime
from flask import session #render_template, request, jsonify
import sqlite3, json, sys
import hashlib, binascii, os

class User():
    def __init__(self, username="", email="", password_hash="", about_me="", last_seen=datetime(1, 1, 1)):
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.about_me = about_me
        self.last_seen = last_seen
    
    # def __repr__(self):
    #     return '<User {}>'.format(self.username)

    # def set_password(self, password):
    #     self.password_hash = hash_password(password)
    
    @staticmethod
    def get_user(username, password):
        db=database.make_db_connection()
        cur=db.cursor()
        cur.execute('SELECT * From Users WHERE username=?', (username,))
        row=cur.fetchone()

        if ((row is not None) and User.verify_password(row[3], password)):
            user=User(row[1],row[2],row[3],row[4],row[5])
            return user
        else:
            return None
        database.close_db_connection(db)

    @staticmethod
    def user_exists(username, email):
        db=database.make_db_connection()
        cur=db.cursor()

        cur.execute('SELECT * From Users WHERE username=? or email=?', (username,email))
        existing_users=cur.fetchall()

        database.close_db_connection(db)        

        if not existing_users:              
            return False # no user exists with that username / email
        else:            
            return True # user exists

    def login_user(self):
        session['username'] = self.username

    def check_password(self, password):
        return verify_password(self.password_hash, password)

    def update_last_seen(username,last_seen):
        db=database.make_db_connection()
        cur=db.cursor()
        cur.execute("Update Users Set last_seen=? Where username=?", (last_seen, username))
        db.commit()
        database.close_db_connection(db)

#     def avatar(self, size):
#         digest = md5(self.email.lower().encode('utf-8')).hexdigest()
#         return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
#             digest, size)

#     def follow(self, user):
#         if not self.is_following(user):
#             self.followed.append(user)

#     def unfollow(self, user):
#         if self.is_following(user):
#             self.followed.remove(user)

#     def is_following(self, user):
#         return self.followed.filter(
#             followers.c.followed_id == user.id).count() > 0

#     def followed_posts(self):
#         followed = Post.query.join(
#             followers, (followers.c.followed_id == Post.user_id)).filter(
#                 followers.c.follower_id == self.id)
#         own = Post.query.filter_by(user_id=self.id)
#         return followed.union(own).order_by(Post.timestamp.desc())
    
#     def get_reset_password_token(self, expires_in=600):
#         return jwt.encode(
#             {'reset_password': self.id, 'exp': time() + expires_in},
#             app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

#     @staticmethod
#     def verify_reset_password_token(token):
#         try:
#             id = jwt.decode(token, app.config['SECRET_KEY'],
#                             algorithms=['HS256'])['reset_password']
#         except:
#             return
#         return User.query.get(id)
    @staticmethod
    def hash_password(password):
        """Hash a password for storing."""
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
                                    salt, 100000)
        pwdhash = binascii.hexlify(pwdhash)
        return (salt + pwdhash).decode('ascii')

    @staticmethod
    def verify_password(stored_password, provided_password):
        """Verify a stored password against one provided by user"""
        salt = stored_password[:64]
        stored_password = stored_password[64:]
        pwdhash = hashlib.pbkdf2_hmac('sha512', 
                                    provided_password.encode('utf-8'), 
                                    salt.encode('ascii'), 
                                    100000)
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')

        # # To Print on console
        # print('This is error ' +pwdhash)
        # print('This is error ' +stored_password)
        # sys.stdout.flush()
        return pwdhash == stored_password

# @login.user_loader
# def load_user(id):
#     return User.query.get(int(id))

# class Post(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     body = db.Column(db.String(140))
#     timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

#     def __repr__(self):
#         return '<Post {}>'.format(self.body)

class database():
    def make_db_connection():
        db = sqlite3.connect("Flask_Sqlite3_Database.db")
        return db

    def close_db_connection(db):
        db.close()
        return