import database
import os

def generate_api_key(product,user):
  new_api_key = os.urandom(64).encode('base-64')
  try:
    db = database.mysql() 
    db.create_api_key(new_api_key,product,user)
  except Exception as e:
    return {'error' : {'message' : str(e), 'code' : 500 }}
  return {'key' : new_api_key}

def validate_api_key(api_key):
  try:
    db = database.mysql()
    product = db.validate_api_key(api_key)
  except ValueError as e:
    return {'error' : {'message' : str(e), 'code' : 401}}
  except Exception as e:
    return {'error' : {'message' : 'Internal server error', 'code' : 500 }}
  return {'product' : product}

print(validate_api_key("123"))
print(validate_api_key("1234"))
