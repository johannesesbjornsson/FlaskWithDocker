import database
import os

##################################################################
#             Massive Function for adding food product           #
##################################################################
def create_textile_product(name,colour,prod_range,tags,materials):
  if tags:
    tags = list(set(tags))
    tags =  [str(val) for val in tags]  # Converting to string
    tags_resp = validate_tags(list(tags))
  if materials:
    material_resp = validate_materials(materials.keys())  # The keys of the dicionary are the material type, which needs to be validated

  insert_stmt = {'textile': [{'ID': '','Prod_range' : prod_range, 'Colour' : colour }]}  # Creating sql alchemy insert format for textile table
  product_tags = format_single_column_input_with_id('Tag',list(tags))
  if 'error' in product_tags:
    return {'error' : {'message' : 'tags must be a list of strings', 'code' : 422 }}
  elif product_tags:
    insert_stmt['product_tags'] = product_tags

  product_materials =format_material_input(dict(materials))
  if 'error' in product_materials:
    return {'error' : {'message' : 'must be dicionary of dictionaries ({"carrots": {"quantity" : 20, "unit" : "kg" }) ', 'code' : 422 }}
  elif product_materials:
    insert_stmt['product_materials'] =product_materials
  try:
    db = database.mysql() 
    db.create_product(name,'textile',insert_stmt)
    return {'response' : {'message' : 'Product added', 'code' : 201 }}
  except Exception as e:
    return {'error' : {'message' : 'Internal server error', 'code' : 500 }}

##################################################################
#             Massive Function for adding textile product        #
##################################################################
def create_food_product(name,customer,family,tags,materials,allergens):
  if tags:
    tags = list(set(tags))
    tags =  [str(val) for val in tags]  # Converting to string
    tags_resp = validate_tags(list(tags))  
  if materials:
    material_resp = validate_materials(materials.keys())  # The keys of the dicionary are the material type, which needs to be validated
  if allergens:
    allergens = list(set(allergens))
    allergens =  [str(val) for val in allergens]  # Converting to string
    allergen_resp = validate_allergens(list(allergens))

  insert_stmt = {'food': [{'ID': '','Customer' : customer, 'Family' : family }]}  # Creating sql alchemy insert format for food table
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
    return {'error' : {'message' : 'Internal server error', 'code' : 500 }}

##################################################################
#                         Other Functions                        #
##################################################################
def generate_api_key(product,user):  # Creating api key linked to user( not acutally used in this app, but hey )
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

def get_products(product_type):  # Getting products based on type passed
  tables = get_product_related_tables(product_type)
  print(tables)
  if 'error' in tables:
    return tables
  try:
    db = database.mysql()
    products = db.get_products(product_type,tables)
  except Exception as e:
    return {'error' : {'message' : 'Internal server error', 'code' : 500 }}
  formatted_output = format_output(products)
  response = {
    'products': products,
    'entries': len(products),
  }
  return response

def format_output(products):  # Formatting data that is to be provided to the user
  for prod in products:
    if prod['product_materials']:
      billOfMaterials = {}
      for entry in prod['product_materials']: 
        material= entry['material']
        entry.pop('material')
        entry['quantity'] = float(entry['quantity'])
        billOfMaterials[material] = entry
      prod['product_materials'] = billOfMaterials   # Changing materials format from list to dictionary
    prod['billOfMaterials'] = prod.pop('product_materials')  # Changing the name

    if prod['product_tags'] is None:
      prod['product_tags'] = []
    prod['tags'] = prod.pop('product_tags')
    if 'product_allergens' in prod:
      if prod['product_allergens'] is None:
        prod['product_allergens'] = []
      prod['allergens'] = prod.pop('product_allergens')

  return products

def get_product_related_tables(product_type):  # Getting the database tables containing data on type passed
  if product_type == "food":
    return ['product_tags','product_materials','product_allergens']
  elif product_type == "textile":
    return ['product_tags','product_materials']
  else:
    return {'error' : {'message' : 'Internal server error', 'code' : 500 }}


def format_material_input(materials):  # Converting to sqlalchmeny insert format
  formatted_list = []
  try:
    for material in materials:
      insert_format = {'ID': '', 'Material' : material, 'Quantity':  round(materials[material]['quantity'],1), 'Unit':  materials[material]['unit'] }
      formatted_list.append(insert_format)
  except Exception as e:
    return ['error']
  return formatted_list

def format_single_column_input_with_id(column,values):  # Converting to sqlalchmeny insert format
  formatted_list = []
  try:
    for value in values:
      insert_format = {'ID': '', column : value}
      formatted_list.append(insert_format)
  except Exception as e:
    return ['error']
  return formatted_list 

def validate_allergens(allergens):  # Checking existing tags to see if they exist, if not adding them to datase
  try:
    db = database.mysql()
    existing_allergens = db.get_allergens(allergens)
    allergens_to_insert = remove_existing(allergens,existing_allergens)
    if allergens_to_insert:
      allergens_formatted = format_single_column_insert_values('Allergen',allergens_to_insert)
      db.add_to_single_column_table('allergens',allergens_formatted)
  except Exception as e:
    return {'error' : {'message' : 'Internal server error', 'code' : 500 }}
  return 0

def validate_tags(tags):  # Checking existing tags to see if they exist, if not adding them to datase
  try:
    db = database.mysql()
    existing_tags = db.get_tags(tags)
    tags_to_insert = remove_existing(tags,existing_tags)
    if tags_to_insert:
      tags_formatted = format_single_column_insert_values('Tag',tags_to_insert)
      db.add_to_single_column_table('tags',tags_formatted)
  except Exception as e:
    return {'error' : {'message' : 'Internal server error', 'code' : 500 }}
  return 0

def validate_materials(materials):  # Checking existing materials to see if they exist, if not adding them to datase
  try:
    db = database.mysql()
    existing_materials = db.get_materials(materials)
    materials_to_insert = remove_existing(materials,existing_materials)
    if materials_to_insert:
      materials_formatted = format_single_column_insert_values('Material',materials_to_insert)
      db.add_to_single_column_table('materials',materials_formatted)
  except Exception as e:
    return {'error' : {'message' : 'Internal server error', 'code' : 500 }}
  return 0

def format_single_column_insert_values(column,values):  #  Create insert statment(s) compatible for sqlalchemy 
  insert_list =[]
  for value in values:
    insert_list.append({column: value})
  return insert_list

def remove_existing(values,existing_values):   # Removing entries from values that is in existing values
  values_lower =  [str(val).lower() for val in values]  # converting all values to lowercase strings
  for tupl in existing_values:
    values_lower = list(filter((tupl[0]).__ne__, values_lower))  # removing all entries of strings equal to tupl
  values_lower = list(set(values_lower))   # removing duplicate values
  return values_lower

