#!/usr/bin/env python3

import os, re, sys, calendar, requests, urllib.request
from random import randrange
from datetime import date, datetime, timedelta
from flask import Flask, abort, jsonify, request, render_template

app = Flask(__name__.split('.')[0])

def randomDate(start, end):
    """
    Return a random datetime between two dates
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)

def randomURI(dateNow):
    """
    Generate a random URI since 2018-12-10, website migrated to WordPress platform and now
    """
    dateInt = datetime.strptime('2018-12-10', '%Y-%m-%d')
    dateRandom = randomDate(dateInt, dateNow)
    dateRandomY = str(dateRandom).split('-')[0]
    dateRandomM = str(dateRandom).split('-')[1]
    dateRandomD = str(dateRandom).split('-')[2].split(' ')[0]
    uri = "{}/{}/{}/".format(dateRandomY, dateRandomM, dateRandomD)
    return uri

def getURL(url):
    """
    Get content from website and return a picture URL
    """
    picture_url = ""
    retries_max = 10
    retries_now = 0
    while picture_url == "" and retries_now <= retries_max:
        content = urllib.request.urlopen(url)
        filtered = re.search(r'<img class="alignnone .+" src="(.+)\?resize=.+" alt .+ data-lazy-srcset="', str(content.read()))
        if not filtered:
            retries_now = retries_now + 1
            continue
        picture_url = filtered.group(1)
        break
    if not picture_url or picture_url == "":
        return None
    else:
        return picture_url

@app.route('/')
def index():
    """
    Return index page from HTML template
    """
    return render_template('index.html')

@app.route('/api/ping')
def ping():
    """
    Return pong response
    """
    return jsonify(response = "pong")

@app.route('/api/version')
def version():
    """
    Return application version
    """
    return jsonify(response = "1.6.0")

@app.route('/api/latest')
def latest():
    """
    Return latest picture URL
    """
    dtoday = date.today()
    dname = calendar.day_name[dtoday.weekday()]
    return jsonify(
        node = os.environ['HOSTNAME'],
        title = "BonjourMadame, {} {} (latest)".format(str(dname), str(dtoday.day)),
        description = "Return latest picture URL",
        url = getURL("http://www.bonjourmadame.fr/"))

@app.route('/api/random')
def random():
    """
    Return random picture URL
    """
    dtoday = date.today()
    dname = calendar.day_name[dtoday.weekday()]
    dateNow = datetime.strptime(datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d')
    return jsonify(
        node = os.environ['HOSTNAME'],
        title = "BonjourMadame, {} {} (random)".format(str(dname), str(dtoday.day)),
        description = "Return random picture URL",
        url = getURL("http://www.bonjourmadame.fr/{}".format(randomURI(dateNow))))

if __name__ == '__main__':
    app.run()
