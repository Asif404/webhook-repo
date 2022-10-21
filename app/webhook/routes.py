import collections
import datetime
from textwrap import indent
from time import time
from typing import Collection
from flask import Blueprint, json, request,render_template
from bson.json_util import dumps
from ..extensions import mongo

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')


 #endpoint for pull-request
@webhook.route('/pullrequest', methods=["POST"])
def pull():
    timestamp =datetime.datetime.utcnow().strftime("%d %B %Y - %I:%M%p UTC")

    if request.headers['Content-Type'] =='application/json':
        val =request.json
        request_id= str(val['repository']['id'])
        author= val['pull_request']['base']['user']['login']
        pullvar=mongo.db.webhook
        from_branch= val['pull_request']['base']['ref']
        to_branch= val['pull_request']['head']['ref']


        if val['action'] == 'opened':
            action="PULL REQUEST"
            pullvar.insert_one({'request_id':request_id,'author':author,'action':action,'from_branch':from_branch,'to_branch':to_branch,'timestamp':timestamp})


        if  val['pull_request']['merged']==True:
            action="MERGE"
            print("MERDEDDDDD")
            pullvar.insert_one({'request_id':request_id,'author':author,'action':action,'from_branch':from_branch,'to_branch':to_branch,'timestamp':timestamp})

    return "200"

#endpoint for push request
@webhook.route('/pushrequest', methods=["POST"])
def push():
    
    timestamp =datetime.datetime.utcnow().strftime("%d %B %Y - %I:%M%p UTC")


    if request.headers['Content-Type'] =='application/json':
        val =request.json     
        request_id= val['after']
        author= val['commits'][0]['author']['username']
        branch=val['ref']
        from_branch=branch.split('/')[2]
        action="PUSH"
        to_branch="null"
        pushvar=mongo.db.webhook
        pushvar.insert_one({'request_id':request_id,'author':author,'action':action,'from_branch':from_branch,'to_branch':to_branch,"timestamp":timestamp})
        return "200"
        

@webhook.route('/')
def home():
    return render_template('index.html')


@webhook.route('/list')
def sendlist():
    collections=mongo.db.webhook.find()
    return dumps(collections)
    

