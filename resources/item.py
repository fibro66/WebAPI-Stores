from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel



class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!")

    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Everey item needs a store id!")

    @jwt_required()  # Requires authentivcation before Get can be run
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()   ## since item is now an object of type ItemModel we has to call json method


    def post(self, name):
        item = ItemModel.find_by_name(name)
        if item: 
            return {'message':"An item with name '{}' already exist".format(name)},400
        
        data = Item.parser.parse_args()          
        item = ItemModel(name,data['price'], data['store_id'])
        try:
            item.save_to_db()
        except:
            return {"message":"An error occurred inserting the item."}, 500 ## 500 is internal server error
        
        return item.json(), 201
    
    def delete(self,name):## we will delete item with specified name        
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            
        return {"message":"Item deleted!"}

    def put(self,name):
        data = Item.parser.parse_args()
        print("Data {0}".format(data['price']))        
        item = ItemModel.find_by_name(name)
        
        if item is None:
            item = ItemModel(name,data['price'],data['store_id']) 
        else:
            item.price = data['price']            

        try:
            item.save_to_db()
        except:
            return {"message":"An error ocurred when updating database"}   
        return item.json()





           

class ItemList(Resource):
    def get(self):
        return {'items:': [ item.json() for item in ItemModel.query.all()] }
    
## alternatively:
##     return {'items:': list(map(lambda x: x.json(), ItemModel.query,all()))}
