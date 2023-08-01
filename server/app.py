#!/usr/bin/env python3

from models import db, Activity, Camper, Signup
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api( app )


class Campers( Resource ):

    def get( self ):
        return make_response( [ c.to_dict( rules = ( '-signups', ) ) 
            for c in Camper.query.all() ] )

api.add_resource( Campers, '/campers' )


class CampersById( Resource ):

    def get( self, id ):
        camper = Camper.query.filter_by( id = id ).first()
        if not camper:
            return make_response( 
                { 'error': 'can not find that camper!' }, 404 
            )
        return make_response( camper.to_dict() )

    def patch( self, id ):
        camper = Camper.query.filter_by( id = id ).first()
        if not camper:
            return make_response( 
                { 'error': 'can not find that camper!' }, 404 
            )
        data = request.json

        for key in data:
            try:
                setattr( camper, key, data[key] )
            except ValueError as v_error:
                return make_response( { 'errors': [ str( v_error ) ] }, 422 )

        db.session.commit()

        return make_response( camper.to_dict() )

        

        

api.add_resource( CampersById, '/campers/<int:id>')





@app.route('/')
def home():
    return ''

if __name__ == '__main__':
    app.run(port=5555, debug=True)
