from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, Inventory, inventory_schema, inventorys_schema, User

api = Blueprint("api", __name__, url_prefix='/api')
@api.route('/inventory', methods = ['POST', "PUT"])
@token_required
def create_inventory(current_user_token):
    # print(request.get_json())
    make = request.json['make']
    model = request.json['model']
    year = request.json['year']
    color = request.json['color']
    user_token = current_user_token.token
    print(user_token,make,color)
    print(f'BIG TESTER:  {user_token}')

    inventory = Inventory(make,model,year, user_token, color)

    db.session.add(inventory)
    db.session.commit()

    response = inventory_schema.dump(inventory)
    return jsonify(response)
    
@api.route('/inventory', methods=['GET'])
@token_required
def get_inventory(current_user_token):
    a_user = current_user_token.token
    inventory = Inventory.query.filter_by(user_token = a_user).all()
    response = inventorys_schema.dump(inventory)
    return jsonify(response)

@api.route('/inventory/<id>', methods = ["GET"])
@token_required
def get_single_car(current_user_token, id):
    inventory = Inventory.query.get(id)
    response = inventory_schema.dump(inventory)
    return jsonify(response)

@api.route('/inventory/<id>', methods = ['POST', "PUT"])
@token_required
def update_contact(current_user_token, id):
    inventory = Inventory.query.get(id)
    inventory.make = request.json['make']
    inventory.model = request.json['model']
    inventory.year = request.json['year']
    inventory.color = request.json['color']
    inventory.user_token = current_user_token.token

    db.session.commit()
    response = inventory_schema.dump(inventory)
    return jsonify(response)

@api.route('/inventory/<id>', methods = ['DELETE'])
@token_required
def delete_inventory(current_user_token, id):
    inventory = Inventory.query.get(id)
    db.session.delete(inventory)
    db.session.commit()
    response = inventory_schema.dump(inventory)
    return jsonify(response)

@api.route('/signin', methods =["POST"])
def sign_up():
    user = User.query.get()
                                                                                