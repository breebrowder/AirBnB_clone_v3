#!/usr/bin/python3
""" Create a new view for Place objects that handles default API actions """
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.user import User
from models.place import Place
import json


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def places(city_id):
    """ Will retrieve all places """
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)
    theList = []
    for place in storage.all('Place').values():
        if(place.city_id == city_id):
            theList.append(place.to_dict())
    return jsonify(theList)


@app_views.route('/places/<place_id>', methods=['GET'])
def place_by_id(place_id):
    """ Get list of all places by id """
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place_id(place_id):
    """ Delete a place by id """
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    obj.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places/', methods=['POST'])
def post_place_id(city_id):
    """ Return place with new status code """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    place = request.get_json()
    if not place:
        abort(400, "Not a JSON")
    if 'user_id' not in place:
        abort(400, "Missing user_id")
    user = storage.get(User, place['user_id'])
    if user is None:
        abort(404)
    if 'name' not in place:
        abort(400, "Missing name")
    place['city_id'] = city_id
    p_var = Place(**place)
    storage.new(p_var)
    storage.save()
    return(p_var.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def put_places_id(place_id):
    """ Return place with new status code """
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    place = request.get_json()
    if place is None:
        abort(400, "Not a JSON")
    for key, value in place.items():
        if key not in ['id', 'user_id', 'created_at', 'updated_at', 'city_id']:
            setattr(obj, key, value)
    obj.save()
    return jsonify(obj.to_dict()), 200
