from flask import Flask, render_template, request
import json
from lambda333.data_model import DB
from lambda333.twitter import upsert_user
from os import path
from lambda333.ml import predict_most_likely_author


def create_app():

    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    DB.init_app(app)

    @app.route('/')
    def landing():
        if not path.exists(app.config['SQLALCHEMY_DATABASE_URI']):
            #DB.drop_all()
            #DB.create_all()
            #DB.session.commit()
            pass
        with open('lambda333/landing.json') as f:
            args = json.load(f)
        return render_template('base.html', **args)

    @app.route('/add_user', methods=['GET'])
    def add_user():
        twitter_handle = request.args['twitter_handle']
        upsert_user(twitter_handle)
        return 'insert successful'


    @app.route('/predict_author', methods=['GET'])
    def predict_author():
        tweet_to_classify = request.args['tweet_to_classify']
        return predict_most_likely_author(tweet_to_classify, ['cher', 'barackobama'])

    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return 'database refreshed'

    return app


#if __name__ == "__main__":
    #create_app().run(host='127.0.0.1', port=5000)

#predict_author?tweet_to_classify=immigrants%20are%20important
#add_user?twitter_handle=barackobama
