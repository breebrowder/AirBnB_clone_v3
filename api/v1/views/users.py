#!/usr/bin/python3
""" Create a new view for User objects that handles default API actions """
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.user import User
import json


@app_views.route('/users', methods=['GET'])
def users():
    """ Will retrieve all users """
    theList = []
    for user in storage.all('User').values():
        theList.append(user.to_dict())
    return jsonify(theList)


@app_views.route('/users/<user_id>', methods=['GET'])
def user_by_id(user_id):
    """ Get list of all users by id """
    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_id(user_id):
    """ Delete a user by id """
    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)
    obj.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/users/', methods=['POST'])
def post_users_id():
    """ Return user with new status code """
    user = request.get_json()
    if not user:
        abort(400, "Not a JSON")
    if 'email' not in user:
        abort(400, "Missing email")
    if 'password' not in user:
        abort(400, "Missing password")
    u_var = User(**user)
    storage.new(u_var)
    storage.save()
    return(u_var.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def put_users_id(user_id):
    """ Return user with new status code """
    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)
    user = request.get_json()
    if user is None:
        abort(400, "Not a JSON")
    for key, value in user.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(obj, key, value)
    obj.save()
    return jsonify(obj.to_dict()), 200
