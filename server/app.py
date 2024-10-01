# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Pet

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

# views 
@app.route('/')
def index():
    return make_response('<h1>Welcome to the pet directory</h1>', 200)

@app.route('/pets/<int:id>')
def pet_by_id(id):
    pet = Pet.query.filter(Pet.id == id).first()

    if pet:
        resp_body = f"<p>{pet.name} {pet.species}</p>"
        resp_status = 200
    else:
        resp_body = f"<p>Pet {pet.id} not found</p>"
        resp_status = 404

    return make_response(resp_body, resp_status)

@app.route('/species/<string:species>')
def pet_by_species(species):
    pets = Pet.query.filter_by(species=species).all()

    total_pets = len(pets)
    resp_body = f"<h2> There are {total_pets} {species}</h2>"

    for pet in pets:
        resp_body += f'<p>{pet.name}</p>'
    return make_response(resp_body, 200)    


if __name__ == '__main__':
    app.run(port=5555, debug=True)
