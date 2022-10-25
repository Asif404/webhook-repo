from flask import Flask
from app.webhook.routes import webhook
from app.webview.routes import webview
from .extensions import mongo

# Creating flask app
def create_app():

    app = Flask(__name__)

    # registering all the blueprints
    app.register_blueprint(webhook)
    app.register_blueprint(webview)

    #config database uri
    app.config['MONGO_URI'] ='mongodb://localhost:27017/flask'

    #initilize mongodb
    mongo.init_app(app)
    return app
