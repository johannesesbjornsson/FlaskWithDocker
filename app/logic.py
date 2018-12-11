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

def get_products(product_type):
  tables = get_product_related_tables(product_type)
  if 'error' in tables:
    return tables
  try:
    db = database.mysql()
    products = db.get_products(product_type,tables)
  except Exception as e:
    return {'error' : {'message' : 'Internal server error', 'code' : 500 }}
  response = {
    'products': products,
    'entries': len(products),
  }
  return response

def get_product_related_tables(product_type):
  if product_type == "food":
    return ['product_tags','product_materials','product_allergens']
  elif product_type == "textile":
    return ['product_tags','product_materials']
  else:
    return {'error' : {'message' : 'Internal server error', 'code' : 500 }}

def create_food_product(name,customer,family,tags,materials,allergens):
  if tags:
    tags_resp = validate_tags(list(tags))
  if materials:
    material_resp = validate_materials(materials.keys())
  if allergens:
    allergen_resp = validate_allergens(list(allergens))

  insert_stmt = {'food': [{'ID': '','Customer' : customer, 'Family' : family }]}
  product_tags = format_single_column_input_with_id('Tag',list(tags))
  if 'error' in product_tags:
    return {'error' : {'message' : 'tags must be a list of strings', 'code' : 422 }}
  elif product_tags:
    insert_stmt['product_tags'] = product_tags

  product_allergens = format_single_column_input_with_id('Allergen',list(allergens))
  if 'error' in product_allergens:
    return {'error' : {'message' : 'allergens must be a list of strings  ', 'code' : 422 }}
  elif product_allergens:
    insert_stmt['product_allergens'] = product_allergens

  product_materials =format_material_input(dict(materials))
  if 'error' in product_materials:
    return {'error' : {'message' : 'must be dicionary of dictionaries ({"carrots": {"quantity" : 20, "unit" : "kg" }) ', 'code' : 422 }}
  elif product_materials:
    insert_stmt['product_materials'] =product_materials
  try:
    db = database.mysql() 
    db.create_product(name,'food',insert_stmt)
    return {'response' : {'message' : 'Product added', 'code' : 201 }}
  except Exception as e:
    return {'error' : {'message' : str(e), 'code' : 500 }}

def format_material_input(materials):
  formatted_list = []
  try:
    for material in materials:
      insert_format = {'ID': '', 'Material' : material, 'Quantity':  materials[material]['quantity'], 'Unit':  materials[material]['unit'] }
      formatted_list.append(insert_format)
  except Exception as e:
    return ['error']
  return formatted_list

def format_single_column_input_with_id(column,values):
  formatted_list = []
  try:
    for value in values:
      insert_format = {'ID': '', column : value}
      formatted_list.append(insert_format)
  except Exception as e:
    return ['error']
  return formatted_list 
##################################################################
##################################################################

def validate_allergens(allergens):
  try:
    db = database.mysql()
    existing_allergens = db.get_allergens(allergens)
  except Exception as e:
    return {'error' : {'message' : 'Internal server error', 'code' : 500 }}
  allergens_to_insert = remove_existing(allergens,existing_allergens)
  if allergens_to_insert:
    allergens_formatted = format_single_column_insert_values('Allergen',allergens_to_insert)
    try:
      db.add_to_single_column_table('allergens',allergens_formatted)
    except Exception as e:
      return {'error' : {'message' : 'Internal server error', 'code' : 500 }}
  return 0

def validate_tags(tags):
  try:
    db = database.mysql()
    existing_tags = db.get_tags(tags)
  except Exception as e:
    return {'error' : {'message' : 'Internal server error', 'code' : 500 }}
  tags_to_insert = remove_existing(tags,existing_tags)
  if tags_to_insert:
    tags_formatted = format_single_column_insert_values('Tag',tags_to_insert)
    try:
      db.add_to_single_column_table('tags',tags_formatted)
    except Exception as e:
      return {'error' : {'message' : 'Internal server error', 'code' : 500 }}
  return 0

def validate_materials(materials):
  try:
    db = database.mysql()
    existing_materials = db.get_materials(materials)
  except Exception as e:
    return {'error' : {'message' : 'Internal server error', 'code' : 500 }}
  materials_to_insert = remove_existing(materials,existing_materials)
  if materials_to_insert:
    materials_formatted = format_single_column_insert_values('Material',materials_to_insert)
    try:
      db.add_to_single_column_table('materials',materials_formatted)
    except Exception as e:
      return {'error' : {'message' : 'Internal server error', 'code' : 500 }}
  return 0

def format_single_column_insert_values(column,values):
  insert_list =[]
  for value in values:
    insert_list.append({column: value})
  return insert_list

def remove_existing(values,existing_values):
  for tupl in existing_values:
    if tupl[0] in values:
      values.remove(tupl[0])
  return values

