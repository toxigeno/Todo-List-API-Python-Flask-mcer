"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Todo
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

#** empieza codes para Todos **
# GET para Todos - probado y funcionando en Postman
@app.route('/todo', methods=['GET'])
def get_todo():
    query = Todo.query.all()
    alltodos = list(map(lambda t: t.serialize(), query))
    return jsonify(alltodos),200

# POST para Todos - probado y funcionando en Postman
@app.route('/todo', methods=['POST'])
def add_new_todo():
    req = request.get_json()
    todo = Todo(label=req["label"], done=req["done"])
    db.session.add(todo)
    db.session.commit()
    return("New Todo Added Successfully")

# Delete para Todos - probado y funcionando en Postma
@app.route('/todo/<int:position>', methods=['DELETE'])
def delete_todo(position):
    todo = Todo.query.get(position)
    if todo is None:
        raise APIException('Todo does not exist', status_code=404)
    db.session.delete(todo)
    db.session.commit()
    return ("Task was deleted")


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
