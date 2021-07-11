from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
            type=float,
            required=True,
            help="This field cannot be left blank!!"
        )

    parser.add_argument('store_id',
            type=int,
            required=True,
            help="every item needs a srote id"
        )


    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if not item:
            return {'message': 'Item not fount'}, 404
        return item.json()


    def post(self, name):
        if ItemModel.find_by_name(name):
            return{'Message': "An item with name '{}' already exist.".format(name)}, 400

        data = Item.parser.parse_args()
        
        item = ItemModel(name, data['price'], data['store_id'])

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item"}, 500  # Internal server error

        return item.json(), 201


    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': "Item '{}' deleted".format(name)}

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, data['price'], data['store_id'])
        else:
            item.price = data['price']
        
        item.save_to_db()
        return item.json()


class ItemsList(Resource):
    def get(self):
        return {'items': [item.json() for item in  ItemModel.query.all()]}