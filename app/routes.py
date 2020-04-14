from app import app
from flask import render_template, request, jsonify
import sqlite3, json, sys
import hashlib, binascii, os

# db = sqlite3.connect("Flask_Sqlite3_Database.db")


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Daniyal'}
    posts = [
        {
            'author': {'username': 'Saad'},
            'body': '''Hello guys!! Today's video is goin to be awesom !'''
        },
        {
            'author': {'username': 'Nabil'},
            'body': 'ok guys lets start todays tutorial'
        },
        {
            'author': {'username': 'Gates'},
            'body': 'Windows is the best'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        db=make_db_connection()
        cur=db.cursor()
        try:
            data = request.get_json()

            name = data['_name']
            email = data['_email'] 
            password_hash = hash_password(data['_password_hash']) # named it on purpose
            
            # # To Print on console
            # print('This is error output' +name+email+password_hash)
            # sys.stdout.flush()
 
            #INSERT with style:
            cur.execute("insert into Users (username,email ,password_hash) values (?, ?, ?)", (name, email, password_hash))
            
            # # INSERT with named style:
            # cur.execute("insert into Users (username,email ,password_hash) values (name=:name, email:email, password_hash=:password_hash)", {"name": name, "email": email, "password_hash": password_hash})

            db.commit()
            return json.dumps(True)
        except db.Error as e:            
            db.rollback()
            return(str(e))
        except Exception as e:
            return(str(e))
        finally:
            if db:
                close_db_connection(db)
    else:
        return render_template('register.html', title='Register - New User')

def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')

def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', 
                                  provided_password.encode('utf-8'), 
                                  salt.encode('ascii'), 
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password

def make_db_connection():
    db = sqlite3.connect("Flask_Sqlite3_Database.db")
    return db

def close_db_connection(db):
    db.close()
    return