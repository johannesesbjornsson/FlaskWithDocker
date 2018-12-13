from flask import Flask, request
from flask_restful import Resource, Api,reqparse
import logic 
#import simplejson
app = Flask(__name__)
api = Api(app)

class Products(Resource):
  def get(self):
    parser = reqparse.RequestParser()
    parser.add_argument('key', location='headers',required=True, help='API KEY Required')
    args = parser.parse_args()
    args = parser.parse_args(strict=True)
    api_key = args['key']
    resp = logic.validate_api_key(api_key)
    if 'error' in resp:
      return resp,resp['error']['code']
    product_type = resp['product']
    products = logic.get_products(product_type)
    if 'error' in products:
      return products,products['error']['code']
    return products,200

  def put(self):
    parser = reqparse.RequestParser()
    parser.add_argument('key', location='headers',required=True, help='API KEY Required',type=str)
    parser.add_argument('name', location='json',required=True, help='argument name required',type=str)
    args = parser.parse_args()
    api_key = args['key']
    name = args['name']
    resp = logic.validate_api_key(api_key)
    if 'error' in resp:
      return resp,resp['error']['code']
    product_type = resp['product']

    json = request.get_json()
    
    if product_type == "food":
      fr = self.validate_json_food(json)
      if 'error' in fr:
        return fr, fr['error']['code']
      insert_resp = logic.create_food_product(name,fr['customer'],fr['family'],fr['tags'],fr['billOfMaterials'],fr['allergens'])
    elif product_type == "textile":
      fr = self.validate_json_textile(json)
      if 'error' in fr:
        return fr, fr['error']['code']
      insert_resp = logic.create_textile_product(name,fr['colour'],fr['range'],fr['tags'],fr['billOfMaterials'])

    if 'error' in insert_resp:
      return insert_resp, insert_resp['error']['code']
    return insert_resp, 201

  def validate_json_textile(self,json):
    keys = list(set(json.keys()) - set(['name', 'range','tags','billOfMaterials','colour']))
    if keys:
      return {'error' : {'message' : 'argparse unrecognised argument '+ keys[0], 'code' : 422 }}
    if 'tags' in json:
      if type(json['tags']) != list:
        return {'error' : {'message' : 'argument tags must be list format', 'code' : 422 }}
    else:
      json['tags'] = []
    if 'billOfMaterials' in json:
      if type(json['billOfMaterials']) != dict:
        return {'error' : {'message' : 'argument billOfMaterials must be dictinary format', 'code' : 422 }}
    else:
      json['billOfMaterials'] = []

    if not 'colour' in json:
      json['colour'] = None
    if not 'range' in json:
      json['range'] = None
    return json

  def validate_json_food(self,json):
    keys = list(set(json.keys()) - set(['name', 'family','tags','allergens','billOfMaterials','customer']))
    if keys:
      return {'error' : {'message' : 'argparse unrecognised argument '+ keys[0], 'code' : 422 }}

    if 'tags' in json:
      if type(json['tags']) != list:
        return {'error' : {'message' : 'argument tags must be list format', 'code' : 422 }}
    else:
      json['tags'] = []
    if 'allergens' in json:
      if type(json['allergens']) != list:
        return {'error' : {'message' : 'argument allergens must be list format', 'code' : 422 }}
    else:
      json['allergens'] = []
    if 'billOfMaterials' in json:
      if type(json['billOfMaterials']) != dict:
        return {'error' : {'message' : 'argument billOfMaterials must be dictinary format', 'code' : 422 }}
    else:
      json['billOfMaterials'] = []

    if not 'family' in json:
      json['family'] = None
    if not 'customer' in json:
      json['customer'] = None
    return json

api.add_resource(Products, '/products')

if __name__ == "__main__":
  app.run(host='0.0.0.0',port=80)
