"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
#obtener todos los miembros
def get_all_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200


#obtener un miembro
@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    member = jackson_family.get_member(member_id)
    if member:
        return jsonify(member), 200
    else:
        return jsonify({"Mensaje": "Miembro no encontrado"}), 404

#añadir un miembro nuevo:
@app.route('/member', methods=['POST'])
def add_member():
    try:
        member_data = request.json
        #validaciones de entrada para agregar miembro:
        if not isinstance(member_data.get("first_name"), str) or not isinstance(member_data.get("age"), int):
             return jsonify({"error": "Datos incorrectos"}), 400
        jackson_family.add_member(member_data)
        return jsonify({"mensaje": "miembro correctamente agregado"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        


#eliminar miembro:
@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    result = jackson_family.delete_member(member_id)
    if result:
        return jsonify({"done": True}), 200
    else:
        return jsonify({"error": "Miembro no encontrado"}), 404
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
