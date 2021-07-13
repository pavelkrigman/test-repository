from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemsList
from resources.store import Store,StoreList

from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'Jose'
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()  ## before the first request is executed, this will create the data.db database and all of the tables in it

jwt = JWT(app, authenticate, identity) # JWT will create a new endpoint: # http://127.0.0.1:5000/auth

api.add_resource(Item, '/item/<string:name>') # http://127.0.0.1:5000/item/desk
api.add_resource(ItemsList, '/items') # http://127.0.0.1:5000/items
api.add_resource(UserRegister, '/register') # http://127.0.0.1:5000/register
api.add_resource(Store,'/store/<string:name>') # http://127.0.0.1:5000/store/ikea
api.add_resource(StoreList, '/stores') # http://127.0.0.1:5000/stores


if __name__ == '__main__':
    db.init_app(app)
    #app.run(port=5000, debug=True)


