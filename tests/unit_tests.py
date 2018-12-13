import unittest
import os
import sys
from inspect import getsourcefile
from decimal import Decimal

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
    self.assertEqual(type(prod['product_tags']),list or None)
    self.assertEqual(type(prod['product_materials']),list or None)
    self.assertEqual(type(prod['product_allergens']),list or None)

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
    self.assertEqual(type(prod['product_tags']),list or None)
    self.assertEqual(type(prod['product_materials']),list or None)
    self.assertEqual(type(prod['name']),str)

class TestLogic(unittest.TestCase):

  def test_remove_existing(self):
    result = logic.remove_existing(['some','some_more'],[('some_more',),('some_diff',)])
    self.assertEqual(result, ['some'])
    result_2= logic.remove_existing(['some','some_more','some'],[('some_more',),('some_diff',),('some',)])
    self.assertEqual(result_2, [])
    result_3= logic.remove_existing(['some','Some_more'],[('some_more',),('some_diff',),('some',)])
    self.assertEqual(result_3, [])
    result_4= logic.remove_existing(['Something','Somet'],[('some_more',),('some_diff',),('some',)])
    self.assertEqual(result_4,['somet','something'])
    result_5= logic.remove_existing(['123',1,'1'],[('some_more',),('some',)])
    self.assertEqual(result_5,['1','123'])
  
  def test_format_single_column_insert_values(self):
    column = 'Tag'
    values = ['aaTest_tag','aaTest_tag_2']
    result = logic.format_single_column_insert_values(column,values)
    self.assertEqual(result, [{'Tag' : 'aaTest_tag'},{'Tag': 'aaTest_tag_2'}])

  def test_format_single_column_input_with_id(self):
    column = 'Tag'
    values = ['Testster_tag','Testster_tag_2']
    result =logic.format_single_column_input_with_id(column,values)
    self.assertEqual(result,[{'Tag': 'Testster_tag', 'ID': ''}, {'Tag': 'Testster_tag_2', 'ID': ''}])

  def test_add_food_product(self):
    result = logic.create_food_product('t_name','t_customer','t_family',['t_tags'],{'t_materials': {'quantity' : 20, 'unit' : 'kg' }},['t_allergen'])
    self.assertEqual(result,{'response': {'message': 'Product added', 'code': 201}})

  def test_add_textile_product(self):
    result = logic.create_textile_product('t_name','t_colour','t_range',['t_tags'],{'t_materials': {'quantity' : 20.00, 'unit' : 'kg' }})
    self.assertEqual(result,{'response': {'message': 'Product added', 'code': 201}})

  def test_get_product_tables(self):
    self.assertEqual(logic.get_product_related_tables('food'), ['product_tags', 'product_materials', 'product_allergens'])
    self.assertEqual(logic.get_product_related_tables('textile'), ['product_tags', 'product_materials'])
    self.assertEqual(logic.get_product_related_tables('NOT A REAL PRODUCT'), {'error': {'message': 'Internal server error', 'code': 500}})

  def test_create_food_product(self):
    materials = {'t_materials': {'quantity' : 20, 'unit' : 'kg' }}
    tags = ['Test_taggggg','Test_tagg_2','Test_tagg_3','Test_tagg_2']
    allergens = ['t_allergen','t_allergen','t_allergen','t_allergen']
    result = logic.create_food_product('test','some customer','a_family',tags,materials,allergens)
    self.assertEqual(result,{'response': {'message': 'Product added', 'code': 201}})

  def test_create_textile_product(self):
    materials = {'t_materials': {'quantity' : 20.0001, 'unit' : 'kg' }}
    tags = ['Test_taggggg','Test_tagg_2','Test_tagg_3','Test_tagg_2']
    result = logic.create_textile_product('test','some_colour','some_range',tags,materials)
    self.assertEqual(result,{'response': {'message': 'Product added', 'code': 201}})

  def test_fail_create_food_product(self):
    materials = {'quantity' : 20, 'unit' : 'kg' }
    tags = ['Test_taggggg','Test_taggg_2','Test_tagg_3','Test_tagg_2']
    tags_2 = ['11',11,'123']
    allergens = ['t_allergen','t_allergen','t_allergen','t_allergen']
    result = logic.create_food_product('test','some customer','a_family',tags,materials,allergens)
    self.assertEqual(result,{'error': {'code': 422, 'message': 'must be dicionary of dictionaries ({"carrots": {"quantity" : 20, "unit" : "kg" }) '}} )
    result_2 = logic.create_food_product('test','some customer','a_family',tags_2,[],allergens)
    self.assertEqual(result_2,{'error': {'message': 'Internal server error', 'code': 500}})

  def test_fail_create_textile_product(self):
    materials = {'quantity' : 20, 'unit' : 'kg' }
    tags = ['Test_taggggg','Test_taggg_2','Test_tagg_3','Test_tagg_2']
    tags_2 = ['11',11,'123']
    result = logic.create_textile_product('test','some_colour','some_range',tags,materials)
    self.assertEqual(result,{'error': {'code': 422, 'message': 'must be dicionary of dictionaries ({"carrots": {"quantity" : 20, "unit" : "kg" }) '}} )
    result_2 = logic.create_textile_product('test','some_colour','some_range',tags_2,[])
    self.assertEqual(result_2,{'error': {'message': 'Internal server error', 'code': 500}})

  def test_format_output(self):
    products = [{'id': 27, 'name': 'some_name', 'family': None, 'customer': None, 'product_tags': [{'tag': 'hey'}, {'tag': 'This'}], 'product_materials': [{'material': 'ca rrots', 'quantity': Decimal('20.0'), 'unit': 'kg'}], 'product_allergens': None}]
    resp = logic.format_output(products)
    self.assertEqual(resp, [{'customer': None, 'allergens': [], 'name': 'some_name', 'family': None, 'tags': [{'tag': 'hey'}, {'tag': 'This'}], 'billOfMaterials': {'ca rrots': {'unit': 'kg', 'quantity': 20.0}}, 'id': 27}])
    products_2 = [{'id': 27, 'name': 'some_name', 'colour': 'red', 'range': 'r', 'product_tags': ['tag'], 'product_materials':[] }]
    resp_2 = logic.format_output(products_2)
    self.assertEqual(resp_2, [{'name': 'some_name', 'tags': ['tag'], 'colour': 'red', 'range': 'r', 'billOfMaterials': [], 'id': 27}])

if __name__ == '__main__':
  unittest.main()
