from app import app
from flask import render_template, request, jsonify, flash, redirect, url_for, session
import sqlite3, json, sys, datetime
from app.models import User, database #, Post
from datetime import datetime

@app.before_request
def before_request_func():
    rule = request.url_rule # Get current route

    urls_to_skip=['/login','/register']
    current_user=session.get('current_user')

    if (rule.rule in urls_to_skip):
        pass # skip user logged in check if route is login or register
    elif current_user is None: # if user is not logged in
        return redirect(url_for('login'))

    # if user is logged in then update last seen
    if current_user is not None:
        user_id=session['current_user'].get('id')
        User.update_last_seen(user_id,str(datetime.utcnow()))
    return

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        db=database.make_db_connection()
        cur=db.cursor()
        body = request.form.get('post')
        user_id=session['current_user'].get('id')

        body = request.form.get('post')

        #INSERT with style:
        cur.execute("insert into Posts (body ,timestamp, author_id) values (?, ?, ?)", (body, datetime.now().isoformat(' ', 'seconds'), user_id))
        db.commit()
        flash('Your post is now live!')
        return redirect(url_for('index'))
    
    user = {'username': session['current_user'].get('username')}
    posts=[]
    
    db=database.make_db_connection()
    cur=db.cursor()
    cur.execute('SELECT a.*,b.username \
        From Posts a Join Users b on a.author_id = b.id' 
            )
    res=cur.fetchall()

    for r in res:
        posts.append({'username': r['username'],'body': r['body']})
    database.close_db_connection(db)

    return render_template('index.html', title='Home', user=user, posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    logout();    #logout if loggedin user visits login route manually   
    if request.method == 'POST':
        data = request.get_json()
        username = data['_username']
        password_hash = data['_password_hash'] # named it on purpose
        user = User.get_user(username,password_hash)

        if user is None:
            flash('Invalid username or password', 'alert alert-danger') #  flash with category
            return jsonify(dict(redirect=url_for('login')))
        user.login_user() #, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return jsonify(dict(redirect=next_page)) 
    return render_template('login.html', title='Sign In')

@app.route('/logout')
def logout():
    if 'current_user' in session:
        session.pop('current_user')
    return redirect(url_for('login'))

@app.route('/register', methods=['GET','POST'])
def register():
    logout();    #logout if loggedin user visits register route manually
    if request.method == 'POST':
        db=database.make_db_connection()
        cur=db.cursor()
        try:
            data = request.get_json()

            name = data['_name']
            email = data['_email']                     

            if (User.user_exists(name,email)):
                flash('username or email already exists', 'alert alert-danger') #  flash with category
                return jsonify(dict(redirect=url_for('register')))        
                        
            password_hash = User.hash_password(data['_password_hash']) # named it on purpose
            
            #INSERT with style:
            cur.execute("insert into Users (username,email ,password_hash) values (?, ?, ?)", (name, email, password_hash))
            
            # # INSERT with named style:
            # cur.execute("insert into Users (username,email ,password_hash) values (name=:name, email:email, password_hash=:password_hash)", {"name": name, "email": email, "password_hash": password_hash})

            db.commit()

            ## TO DO i.e. save username in session then redirect to index page
            flash('Registration Successful... Please login', 'alert alert-success') #  flash with category
            return jsonify(dict(redirect=url_for('login')))
        # except db.Error as e:
        #     db.rollback()
        #     flash('Error' + str(e) , 'alert alert-danger') #  flash with category
        #     return jsonify(dict(redirect=url_for('register')))
        except Exception as e:
            db.rollback()
            flash('Error' + str(e) , 'alert alert-danger') #  flash with category
            return jsonify(dict(redirect=url_for('register')))
        finally:
            if db:
                database.close_db_connection(db)
    else:
        return render_template('register.html', title='Register - New User')