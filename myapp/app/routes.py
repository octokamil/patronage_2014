#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request
import json, os, urllib, datetime

app = Flask(__name__)

def main():
    print "Starting app"
    global superheroes
    superheroes = load_file()
    app.run()
    
def load_file():
    if not os.path.exists('superheros.json'):
        open('superheros.json', 'w').close() 
    else:
        return json.loads(open('superheros.json').read())

def update_file():
    jsonFile = open("superheros.json", "w+")
    jsonFile.write(json.dumps(superheroes))
    jsonFile.close()

@app.route('/superheros', methods = ['GET'])
def get_heros():
    return jsonify( { 'superheroes': superheroes } ), 200

@app.route('/superheros/<superhero_name>', methods = ['GET'])
def get_hero(superhero_name):
    hero = filter(lambda t: t['name'] == superhero_name, superheroes)
    if len(hero) == 0:
        abort(404)
    return jsonify( { 'hero': hero[0] } )

@app.route('/')
def hello():
    return 'Super Heroes App!'

@app.route('/superheros/<superhero_name>', methods = ['DELETE'])
def delete_hero(superhero_name):
    hero = filter(lambda t: t['name'] == superhero_name, superheroes)
    if len(hero) == 0:
        abort(404)
    superheroes.remove(hero[0])
    update_file()
    return '', 204

@app.route('/superheros', methods = ['POST'])
def create_hero():
    
    if not request.json:
        abort(make_response("No data", 400))

    name = filter(lambda m: m['name'] == request.json['name'], superheroes)
# name validation
    if not 'name' in request.json:
        abort(make_response(jsonify( { 'name': 'Object requires name to be created' } ), 400)) 
    if len(name) != 0:
        abort(make_response(jsonify( { 'name': 'Object with the same name already exist!' } ), 400))
    if len(request.json['name']) > 20:
        abort(make_response(jsonify( { 'name': 'Name violates maximum length of 20 characters' } ), 400))
# real name validation
    if not 'real_name' in request.json:
        abort(make_response(jsonify( { 'real_name': 'Object requires real name to be created' } ), 400)) 
    if len(request.json['real_name']) > 50:
        abort(make_response(jsonify( { 'real_name': 'Real name violates maximum length of 20 characters' } ), 400))
# appearance date validation
    if not 'appearance_date' in request.json:
        abort(make_response(jsonify( { 'appearance_date': 'Object requires appearance_date to be created' } ), 400)) 
    try:
        datetime.datetime.strptime(request.json['appearance_date'],'%m-%Y')
    except ValueError:
        abort(make_response(jsonify( { 'appearance_date': 'Invalid date format' } ), 400))
# url validation
    try:
        urllib.urlopen(request.json['web_page'])
    except IOError:
        abort(make_response(jsonify( { 'web_page': 'Invalid URL' } ), 400)) 


    hero = {
        'name': request.json['name'],
        'real_name': request.json['real_name'],
        'appearance_date': request.json['appearance_date'],
        'web_page': request.json['web_page']
    }
    superheroes.append(hero)
    update_file()
    return jsonify( { 'hero': hero } ), 201

@app.route('/superheros/<superhero_name>', methods = ['PUT'])
def update_hero(superhero_name):
    hero = filter(lambda t: t['name'] == superhero_name, superheroes)
    if len(hero) == 0:
        abort(make_response("Not found", 404))
    if not request.json:
        abort(make_response("No data", 400))
# name validation        
    if len(request.json['name']) > 20:
        abort(make_response(jsonify( { 'name': 'Name violates maximum length of 20 characters' } ), 400))
# real name validation
    if len(request.json['real_name']) > 50:
        abort(make_response(jsonify( { 'real_name': 'Real name violates maximum length of 20 characters' } ), 400))
# appearance date validation
    if not 'appearance_date' in request.json:
        abort(make_response(jsonify( { 'appearance_date': 'Object requires appearance_date to be created' } ), 400)) 
    try:
        datetime.datetime.strptime(request.json['appearance_date'],'%m-%Y')
    except ValueError:
        abort(make_response(jsonify( { 'appearance_date': 'Invalid date format' } ), 400))
# url validation
    try:
        urllib.urlopen(request.json['web_page'])
    except IOError:
        abort(make_response(jsonify( { 'web_page': 'Invalid URL' } ), 400)) 



    hero[0]['name'] = request.json.get('name', hero[0]['name'])
    hero[0]['real_name'] = request.json.get('real_name', hero[0]['real_name'])
    hero[0]['appearance_date'] = request.json.get('appearance_date', hero[0]['appearance_date'])
    hero[0]['web_page'] = request.json.get('web_page', hero[0]['web_page'])
    update_file()
    return jsonify( { 'hero': hero[0] } )

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

if __name__ == '__main__':
    main()