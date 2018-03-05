# Job Finder Application

A simple job finder application (Python 3.6, Django 1.11), which can easily be deployed to Heroku.

## Prerequisites

Be sure you have the following installed on your development machine:

+ Python >= 3.5
+ Django >= 1.11
+ Virtualenv
+ Database (either one):
    + MySQL >= 5.6 ([guide]())
    + Postgres >= 9.2 ([guide]())
+ pip


## Running Locally

Make sure you have Python [installed properly](http://install.python-guide.org).

```sh
$ git clone https://github.com/randolphpebenito/try-job-finder-app.git
$ cd try-job-finder-app
$ virtualenv venv -p python3.6 
$ source venv/bin/activate

$ pip install -r requirements.txt
$ cp .env.example .env # Change your designated settings (12 factor app)

$ python manage.py migrate
$ python manage.py createsuperuser # Create your admin user
$ python manage.py collectstatic

$ python manage.py test # THIS IS IMPORTANT
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.............................................................................
----------------------------------------------------------------------
Ran 77 tests in 23.428s

OK
Destroying test database for alias 'default'...


$ python manage.py runserver
Performing system checks...

System check identified no issues (0 silenced).
March 05, 2018 - 12:21:32
Django version 1.11.6, using settings 'myproject.settings'
Starting development server at http://127.0.0.1:8000/


```

Your app should now be running on [localhost:8000](http://localhost:8000/).

## Deploying to Heroku

```sh
$ heroku create
$ git push heroku master

$ heroku run python manage.py migrate
$ heroku open
```
or

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

This application supports the [Getting Started with Python on Heroku](https://devcenter.heroku.com/articles/getting-started-with-python) article - check it out.
