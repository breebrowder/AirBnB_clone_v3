#!/usr/bin/python3
""" Create a new view for Amenity objects that handles default API actions """
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
import json


@app_views.route('/amenites')
def amenities():
    """ Will retrieve all amenities """
    theList = []
    for amenity in storage.all('Amenity').values():
        theList.append(amenity.to_dict())
    return jsonify(theList)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def amenities_by_id(amenity_id):
    """ Get list of all amenities by id """
    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_id(amenity_id):
    """ Delete an amenity by id """
    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        abort(404)
    obj.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities/', methods=['POST'])
def post_amenities_id():
    """ Return amenity with new status code """
    amenity = request.get_json()
    if not amenity:
        abort(400, "Not a JSON")
    if 'name' not in amenity:
        abort(400, "Missing name")
    a_var = Amenity(**amenity)
    storage.new(a_var)
    storage.save()
    return(a_var.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def put_amen_id(amenity_id):
    """ Return amenity with new status code """
    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        abort(404)
    amenity = request.get_json()
    if amenity is None:
        abort(400, "Not a JSON")
    for key, value in amenity.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(obj, key, value)
    obj.save()
    return jsonify(obj.to_dict()), 200
