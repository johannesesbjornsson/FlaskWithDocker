import unittest
import os
import sys
from inspect import getsourcefile

current_path = os.path.abspath(getsourcefile(lambda:0))  # To get parent directory
current_dir = os.path.dirname(current_path)  
parent_dir = current_dir[:current_dir.rfind(os.path.sep)]
sys.path.insert(0, parent_dir+'/app')  # Settig dir to '../app'
import database
import logic

class TestDatabase(unittest.TestCase):
  db=database.mysql()
  def test_api_key_functions(self):  # 5 Tests: create API KEY, fail create API KEY, validate API KEY,delete API KEY and fail delete API KEY
    api_key =  os.urandom(64).encode('base-64') #'AdCEG77a7IK7L9N7O72PaQSTUafafaf727432723afVWYZa1aac'
    product = 'test_prod'
    db = self.db
    self.assertEqual(db.create_api_key(api_key, product, 'some_user'), 0)
    with self.assertRaises(Exception):  # This generated pymsql specifc error so I just check for an exception
      db.create_api_key(api_key,self.product,'some_user')

    self.assertEqual(db.validate_api_key(api_key), product)
    self.assertEqual(db.delete_api_key(api_key), 0)

    with self.assertRaises(ValueError):
      db.delete_api_key(api_key)

  def test_tags(self):
    tags =[{'Tag' : 'Test_tag'},{'Tag': 'Test_tag_2'}]
    db = self.db
    self.assertEqual(db.add_to_single_column_table('tags',tags),0)
    tags_created = ['Test_tag','Test_tag_2']
    self.assertEqual(db.get_tags(tags_created),[('Test_tag',), ('Test_tag_2',)] )
    self.assertEqual(db.delete_tags(tags_created),0)
                        
  def test_allergens(self):
    allergens=[{'Allergen' : 'Test_allergen'},{'Allergen': 'Test_allergen_2'}]
    db = self.db
    self.assertEqual(db.add_to_single_column_table('allergens',allergens),0)
    allergens_created = ['Test_allergen','Test_allergen_2']
    self.assertEqual(db.get_allergens(allergens_created),[('Test_allergen',), ('Test_allergen_2',)] )
    self.assertEqual(db.delete_allergens(allergens_created),0)

  def test_materials(self):
    materials=[{'Material' : 'Test_materials'},{'Material': 'Test_materials_2'}]
    db = self.db
    self.assertEqual(db.add_to_single_column_table('materials',materials),0)
    materials_created = ['Test_materials','Test_materials_2']
    self.assertEqual(db.get_materials(materials_created),[('Test_materials',), ('Test_materials_2',)] )
    self.assertEqual(db.delete_materials(materials_created),0)


  def test_add_product(self):
    db = self.db
    prod_data = {
      'food': [
        {'ID': '','Customer' : 'Some_cust', 'Family' : 'fam' }
      ], 
      'product_tags' : [
        {'Tag': 'Test_tag_11', 'ID': ''},
        {'Tag': 'Test_tag_22', 'ID': ''}
      ],
      'product_materials' : [
          {'ID' : '', 'Material' : 'Test_materials_11', 'Quantity': '20', 'Unit': 'kg' },
          {'ID' : '', 'Material' : 'Test_materials_22', 'Quantity': '10', 'Unit': 'kg' }
      ],
      'product_allergens' : [
          {'ID' : '', 'Allergen' : 'Test_product_allergens'}
      ]
    }
    if not db.get_materials(['Test_materials_11']):
      db.add_to_single_column_table('materials',[{ 'Material': 'Test_materials_11'}])
    if not db.get_materials(['Test_materials_22']):
      db.add_to_single_column_table('materials',[{ 'Material': 'Test_materials_22'}])
    if not db.get_tags(['Test_tag_11']):
      db.add_to_single_column_table('tags',[{ 'Tag': 'Test_tag_11'}])
    if not db.get_tags(['Test_tag_22']):
      db.add_to_single_column_table('tags',[{ 'Tag': 'Test_tag_22'}])
    if not db.get_allergens(['Test_product_allergens']):
      db.add_to_single_column_table('allergens',[{ 'Allergen': 'Test_product_allergens'}])
    self.assertEqual(db.create_product('name','food',prod_data), 0)
    prod = db.get_products('food',['product_tags','product_materials','product_allergens'])[0]
    self.assertEqual(type(prod['id']),int)
    self.assertEqual(type(prod['product_tags']),list)
    self.assertEqual(type(prod['product_materials']),list)
    self.assertEqual(type(prod['product_allergens']),list)
    self.assertEqual(type(prod['customer']),str )
    self.assertEqual(type(prod['family']),str )

  def test_add_product_2(self):
    db = self.db
    prod_data = {
      'textile': [
        {'ID': '','Colour' : 'Blue', 'Prod_range' : 'hispter' }
      ], 
      'product_tags' : [
        {'Tag': 'Test_tag_11', 'ID': ''},
        {'Tag': 'Test_tag_22', 'ID': ''}
      ],
      'product_materials' : [
          {'ID' : '', 'Material' : 'Test_materials_11', 'Quantity': '20', 'Unit': 'kg' },
          {'ID' : '', 'Material' : 'Test_materials_22', 'Quantity': '10', 'Unit': 'kg' }
      ]
    }
    if not db.get_materials(['Test_materials_11']):
      db.add_to_single_column_table('materials',[{ 'Material': 'Test_materials_11'}])
    if not db.get_materials(['Test_materials_22']):
      db.add_to_single_column_table('materials',[{ 'Material': 'Test_materials_22'}])
    if not db.get_tags(['Test_tag_11']):
      db.add_to_single_column_table('tags',[{ 'Tag': 'Test_tag_11'}])
    if not db.get_tags(['Test_tag_22']):
      db.add_to_single_column_table('tags',[{ 'Tag': 'Test_tag_22'}])
    self.assertEqual(db.create_product('name','textile',prod_data), 0)
    prod = db.get_products('textile',['product_tags','product_materials'])[0]
    self.assertEqual(type(prod['id']),int)
    self.assertEqual(type(prod['product_tags']),list)
    self.assertEqual(type(prod['product_materials']),list)
    self.assertEqual(type(prod['name']),str)
    self.assertEqual(type(prod['colour']),str)
    self.assertEqual(type(prod['prod_range']),str)

class TestLogic(unittest.TestCase):

  def test_remove_existing(self):
    result = logic.remove_existing(['some','some_more'],[('some_more',),('some_diff',)])
    self.assertEqual(result, ['some'])
    result_2= logic.remove_existing(['some','some_more'],[('some_more',),('some_diff',),('some',)])
    self.assertEqual(result_2, [])
  
  def test_format_single_column_insert_values(self):
    column = 'Tag'
    values = ['Test_tag','Test_tag_2']
    result = logic.format_single_column_insert_values(column,values)
    self.assertEqual(result, [{'Tag' : 'Test_tag'},{'Tag': 'Test_tag_2'}])

  def test_format_single_column_input_with_id(self):
    column = 'Tag'
    values = ['Test_tag','Test_tag_2']
    result =logic.format_single_column_input_with_id(column,values)
    self.assertEqual(result,[{'Tag': 'Test_tag', 'ID': ''}, {'Tag': 'Test_tag_2', 'ID': ''}])

  def test_add_product(self):
    result = logic.create_food_product('t_name','t_customer','t_family',['t_tags'],{'t_materials': {'quantity' : 20, 'unit' : 'kg' }},['t_allergen'])
    self.assertEqual(result,{'response': {'message': 'Product added', 'code': 201}})

  def test_get_product_tables(self):
    self.assertEqual(logic.get_product_related_tables('food'), ['product_tags', 'product_materials', 'product_allergens'])
    self.assertEqual(logic.get_product_related_tables('textile'), ['product_tags', 'product_materials'])
    self.assertEqual(logic.get_product_related_tables('NOT A REAL PRODUCT'), {'error': {'message': 'Internal server error', 'code': 500}})


if __name__ == '__main__':
  unittest.main()
