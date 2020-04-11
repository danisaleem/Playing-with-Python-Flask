# PSA-Koblenz-Python-Training
Python-Flask training sessions for the students of PSA (Pakistan Students Association) Koblenz. 


## A Brief Introduction

A full stack application using python flask and and a suitable database with it. (MongoDB/SQL).
Python-Flask is a micro web framework written in Python which is used to develop small and large scale web applications. It is easy to use and its also scalable.


# Pre-requisites

## Python, Python-Eve and Python-Flask

One must have Python installed in his local system for working on this Full stack application easily. Other than Python one must also have to install Python-Eve, Python-Flask and its dependencies. To install flask, simply use
```
$ pip install flask
```

# Structure of Application

**App folder**
* It contains static and templates folders which are used to contain html,css, JS and other files. Moreover It also contains init file which declares or initializes the instance of flask app, Other than that it also contains routes.py file which contains definition of all the routes being used in the application.

**Static folder**

* It contains Style sheets and Javascript files. Moreover one can also put any JSON or other files to be used by the application.

**Templates folder**

* It contains the HTML files used via any templating engine that are used by the flask application.

# Running this Web Application

**using basic flask command**
```
$ flask run
```

# Checking the User Interface

https://localhost:5000/


# Few Aspects Related To Using Python-Flask

## Running in Debug Mode

One have to restart it manually after each change to your code. That is not very nice and Flask can do better. If you enable debug support the server will reload itself on code changes, and it will also provide you with a helpful debugger if things go wrong.

To enable all development features (including debug mode) you can export the FLASK_ENV environment variable and set it to development before running the server:
```
$ export FLASK_ENV=development
$ flask run
```
You can also control debug mode separately from the environment by exporting FLASK_DEBUG=1.

## Documentation

This RESTFUL-API is written using Python-Flask, Huge, extensive and detailed documentation for flask is provided (http://flask.pocoo.org/docs/1.0/), Furthermore a very strong support is also there on multiple platform all around the web.
