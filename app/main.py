from flask import Flask, request 
from flask_restful import Resource, Api,reqparse
import logic 

# the all-important app variable:
app = Flask(__name__)
api = Api(app)

#@require_appkey
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
    parser.add_argument('name',required=True, help="argument name required",type=str)
    args = parser.parse_args()
    api_key = args['key']
    name = args['name']
    resp = logic.validate_api_key(api_key)
    if 'error' in resp:
      return resp,resp['error']['code']
    product_type = resp['product']
    
    if product_type == "food":
      family = request.form.get('family', None)
      customer = request.form.get('customer', None)
      materials = request.form.get('billOfMaterials', [])
      allergens = request.form.get('allergens', [])
      tags = request.form.get('tags', [])
      if allergens:
        allergens = allergens.split(',')
      if tags:
        tags= tags.split(',')
      print(materials)
      insert_resp = logic.create_food_product(name,customer,family,tags,materials,allergens)

    if 'error' in insert_resp:
      return insert_resp, insert_resp['error']['code']
    return insert_resp, 201



api.add_resource(Products, '/products')

if __name__ == "__main__":
  app.run(host='0.0.0.0',port=80)
