from flask import Flask, request
from flask_restful import Resource, reqparse
from models.user import UserModel
import sqlite3
from db import db


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {'message': 'User is already present in the system'}, 400
        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created successfully."}, 201
