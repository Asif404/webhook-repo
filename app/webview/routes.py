from flask import Blueprint, render_template
from bson.json_util import dumps
import pymongo
from ..extensions import mongo

webview = Blueprint('Webview', __name__, url_prefix='/webview')


#UI path url
@webview.route('/')
def home():

    return render_template('index.html')

#api to fetch details from database
@webview.route('/api')
def sendlist():

    #get latest 5 data from database
    collections=mongo.db.webhook.find().sort("_id",pymongo.DESCENDING).limit(5)
    return dumps(collections)