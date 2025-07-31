"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def get_all_members():
    # This is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    return jsonify(members), 200


@app.route('/members/<int:member_id>', methods=['GET'])
def get_single_member(member_id):
    member = jackson_family.get_member(member_id)
    if member is None:
        return jsonify({"error": "Member not found"}), 404
    return jsonify(member), 200


@app.route('/members', methods=['POST'])
def add_member():
    try:
        member_data = request.get_json()
        if not member_data:
            return jsonify({"error": "No data provided"}), 400
        
        # Validar campos requeridos
        required_fields = ["first_name", "age", "lucky_numbers"]
        for field in required_fields:
            if field not in member_data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        new_member = jackson_family.add_member(member_data)
        return jsonify(new_member), 200
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500


@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    try:
        success = jackson_family.delete_member(member_id)
        if not success:
            return jsonify({"error": "Member not found"}), 404
        return jsonify({"done": True}), 200
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500



# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
