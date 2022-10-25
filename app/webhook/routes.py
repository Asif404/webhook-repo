
import datetime
from textwrap import indent
from time import time
from typing import Collection
from flask import Blueprint,request

import pymongo
from ..extensions import mongo

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')


 #endpoint for pull-request
@webhook.route('/pullrequest', methods=["POST"])
def pull():

    timestamp =datetime.datetime.utcnow().strftime("%d %B %Y - %I:%M%p UTC")

    #checking if the request content_typer is application/json
    if (request.headers['Content-Type'] =='application/json'):

        #convert request to json
        req =request.json

        #from request body extract the required data
        request_id= str(req['repository']['id'])
        author= req['pull_request']['base']['user']['login']
        to_branch= req['pull_request']['base']['ref']
        from_branch= req['pull_request']['head']['ref']

        #connect to database
        pullreq=mongo.db.webhook


        #check if action type is 'opened' 
        if req['action'] == 'opened':
            action="PULL REQUEST"

            #insert data into database
            pullreq.insert_one({'request_id':request_id,'author':author,'action':action,'from_branch':from_branch,'to_branch':to_branch,'timestamp':timestamp})

        #check if it's megre 
        if  req['pull_request']['merged']==True:
            action="MERGE"

            #insert data into database
            pullreq.insert_one({'request_id':request_id,'author':author,'action':action,'from_branch':from_branch,'to_branch':to_branch,'timestamp':timestamp})

    #return error message
    return "ERROR: Content-type should be application/json"

#endpoint for push request
@webhook.route('/pushrequest', methods=["POST"])
def push():
    
    timestamp =datetime.datetime.utcnow().strftime("%d %B %Y - %I:%M%p UTC")

    #checking if the request content_typer is application/json
    if request.headers['Content-Type'] =='application/json':

        #convert request to json
        req =request.json

        #from request body extract the required data     
        request_id= req['after']
        author= req['commits'][0]['author']['username']
        branch=req['ref']
        from_branch=branch.split('/')[2]
        action="PUSH"
        to_branch="null"

        #connect to database
        pushreq=mongo.db.webhook

        #insert data into database
        pushreq.insert_one({'request_id':request_id,'author':author,'action':action,'from_branch':from_branch,'to_branch':to_branch,"timestamp":timestamp})
        
    #return error message
    return "ERROR: Content-type should be application/json"   





    


