#!/usr/bin/python3
""" Create a new view for Review objects that handles default API actions """
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.user import User
from models.place import Place
from models.review import Review
import json


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def review_for_place(place_id):
    """ Will retrieve all reviews from a place """
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    theList = []
    for review in storage.all('Review').values():
        if(review.place_id == place_id):
            theList.append(review.to_dict())
    return jsonify(theList)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def review_by_id(review_id):
    """ Will retrieve a review """
    obj = storage.get(Review, review_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review_id(review_id):
    """ Delete a review by id """
    obj = storage.get(Review, review_id)
    if obj is None:
        abort(404)
    obj.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews/', methods=['POST'])
def post_review_id(place_id):
    """ Return review with new status code """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    review = request.get_json()
    if not review:
        abort(400, "Not a JSON")
    if 'user_id' not in review:
        abort(400, "Missing user_id")
    user = storage.get(User, review.get('user_id'))
    if user is None:
        abort(404)
    if 'text' not in review:
        abort(400, "Missing text")
    review['place_id'] = place_id
    r_var = Review(**review)
    storage.new(r_var)
    storage.save()
    return(r_var.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def put_reviews_id(review_id):
    """ Return review with new status code """
    obj = storage.get(Review, review_id)
    if obj is None:
        abort(404)
    review = request.get_json()
    if review is None:
        abort(400, "Not a JSON")
    for key, value in review.items():
        if key not in ['id', 'user_id',
                       'place_id', 'created_at', 'updated_at', 'city_id']:
            setattr(obj, key, value)
    obj.save()
    return jsonify(obj.to_dict()), 200
