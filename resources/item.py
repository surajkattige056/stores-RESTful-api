import sqlite3
import sys
sys.path.append("..")
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, JWT
from flask import request
from models.item import ItemModel
from db import db

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type = float,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('store_id',
                        type=float,
                        required=True,
                        help="Every Item requires a store id"
                        )
    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        else:
            return {'message': 'Item not found'}, 404

    @jwt_required()
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, data['price'], data['store_id'])

        try:
            item.save_to_db()
        except:
            return {'message': 'An error occured inserting the item'}, 500 #Internal Server Error
        return item.json(), 201

    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message': "Item '{}' has been deleted from the database".format(name)}

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        print(data['price'])

        item = ItemModel.find_by_name(name)

        if item is None:
            try:
                item = ItemModel(name, data['price'], data['store_id'])
            except:
                return {'message': 'An error occurred inserting the item.'}, 500
        else:
            try:
                item.price = data['price']
            except:
                return {'message': 'An error occurred updating the item.'}, 500
        item.save_to_db()
        return item.json()


class ItemList(Resource):
    @jwt_required()
    def get(self):
        return {'items': list(map(lambda x:x.json(), ItemModel.query.all()))}