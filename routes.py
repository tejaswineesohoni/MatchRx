from flask import render_template, flash, redirect
from flask import Flask
from flask import request
from flask import Markup
from flask_esclient import ESClient
import requests
from elasticsearch import Elasticsearch
from iron_celery import iron_cache_backend
from forms import LoginForm
import matchingpeople
import fetchtweets

app = Flask(__name__)

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
	return render_template('index.html',title='MatchRx')

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm(csrf_enabled=False)
	return render_template('login.html',title='MatchRx Login', form=form)

@app.route('/output', methods=['GET', 'POST'])
def output():
	if request.method=="POST":
		user = request.form['handle']
		fetchtweets.twitterSearch()
		matchingpeople.fillElasticSearch()
		person=matchingpeople.findmatchingpeople(user)
		username,description=fetchtweets.findUser(person)
		return render_template('output.html',title='Matches Found', username=username, description=description)

if __name__=='__main__':
    app.run(debug=True)
