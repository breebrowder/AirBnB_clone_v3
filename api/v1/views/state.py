#!/usr/bin/python3
""" Create a new view for State objects that handles default API actions """
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.state import State
import json


@app_views.routw('/states', methods=['GET'])
def states():
    """ Get list of all state objects """
    theList = []
    for state in storage.all('State').values():
        theList.append(state.to_dict())
    print(theList)
    return jsonify(theList)


@app_views.route('/states/<state_id>', methods=['GET'])
def states_id(state_id):
    """ Get a state object """
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def del_states_id(state_id):
    """ Delete a state object """
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    obj.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/', methods=['POST'])
def post_states_id():
    """ Return state with new status code """
    state = request.get_json()
    if not state:
        abort(400, "Not a JSON")
    if 'name' not in state:
        abort(400, "Missing name")
    state_var = State(**state)
    storage.new(state_var)
    storage.save()
    return(state_var.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def put_states_id(state_id):
    """ Return state with new status code """
    obj = storage.get(State, state_id)
    state = request.get_json()
    if obj is None:
        abort(404)
    if state is None:
        abort(400, "NOt a JSON")
    for key, value in state.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(obj, key, vlaue)
    obj.save()
    return jsonify(obj.to_dict()), 200
