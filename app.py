import os

from flask import Flask
from flask_restful import  Api
from flask_jwt import JWT



from security import authenticate,identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList


app = Flask(__name__)
##app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get ('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get ('sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # This turns off the extension Flask-sql alchemy only
app.secret_key = 'Finn'
api = Api(app)


## JWT creates endpoint /auth. When we calls /auth JWT gets the usernam and password ans sends it
## over to the authenticate function. The authenticate function returns a user, and the JWT class
## returns a token

jwt = JWT(app, authenticate, identity) 

api.add_resource(Store,'/stores/<string:name>')
api.add_resource(Item,'/items/<string:name>')
api.add_resource(ItemList,'/items')
api.add_resource(StoreList,'/stores')
api.add_resource(UserRegister,'/register')

if __name__ == '__main__':
    from db import db
    db.init_app(app)  ## We are importing our Flask-app
    app.run(port=5000, debug=True)
