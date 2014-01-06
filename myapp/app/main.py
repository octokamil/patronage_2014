#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request, Blueprint
import json, os, urllib, datetime
# from validation import Validation
from database import DatabaseManipulation
from routes import superheroes_api, db

app = Flask(__name__)
app.register_blueprint(superheroes_api)

def main():
    print "Starting app"
    db.superheroes = db.load_file("superheros.json")
    app.run()

@app.route('/')
def hello():
    return 'Super Heroes App!'

if __name__ == '__main__':
    main()