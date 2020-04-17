from app import app
from flask import render_template, request, jsonify, flash, redirect, url_for
import sqlite3, json, sys
from app.models import User, database #, Post

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

@app.route('/login', methods=['GET', 'POST'])
@app.route('/log-in', methods=['GET', 'POST'])
def login():    
    if request.method == 'POST':
        data = request.get_json()

        username = data['_username']
        password_hash = data['_password_hash'] # named it on purpose
        
        user = User.get_user(username,password_hash)

        if user is None:
            flash('Invalid username or password')
            return jsonify(dict(redirect=url_for('login')))
        user.login_user() #, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return jsonify(dict(redirect=next_page))
    return render_template('login.html', title='Sign In')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        db=database.make_db_connection()
        cur=db.cursor()
        try:
            data = request.get_json()

            name = data['_name']
            email = data['_email'] 
            password_hash = User.hash_password(data['_password_hash']) # named it on purpose
            
            #INSERT with style:
            cur.execute("insert into Users (username,email ,password_hash) values (?, ?, ?)", (name, email, password_hash))
            
            # # INSERT with named style:
            # cur.execute("insert into Users (username,email ,password_hash) values (name=:name, email:email, password_hash=:password_hash)", {"name": name, "email": email, "password_hash": password_hash})

            db.commit()

            ## TO DO i.e. save username in session then redirect to index page
            return json.dumps(True)
        except db.Error as e:            
            db.rollback()
            return(str(e))
        except Exception as e:
            return(str(e))
        finally:
            if db:
                database.close_db_connection(db)
    else:
        return render_template('register.html', title='Register - New User')