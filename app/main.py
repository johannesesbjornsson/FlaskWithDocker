from flask import Flask 
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
    product = resp['product']
    return {'products': product }, 200

  def put(self):
    todos = request.form['data']
    return {"todo_id": todos}



api.add_resource(Products, '/products')

if __name__ == "__main__":
  app.run(host='0.0.0.0',port=80)
