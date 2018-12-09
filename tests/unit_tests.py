import unittest
import os
import sys
from inspect import getsourcefile

current_path = os.path.abspath(getsourcefile(lambda:0))  # To get parent directory
current_dir = os.path.dirname(current_path)  
parent_dir = current_dir[:current_dir.rfind(os.path.sep)]
sys.path.insert(0, parent_dir+'/app')  # Settig dir to '../app'
import database

class TestDatabase(unittest.TestCase):
  test_api_key =  'ABCEG77a7IK7L9N7O72PaQSTUafafaf727432723afVWYZa1aac'
  database = 'localhost'
  product = 'api_keys'
  user = 'some_user'
  
  def test_api_key_functions(self):  # 5 Tests: create API KEY, fail create API KEY, validate API KEY,delete API KEY and fail delete API KEY
    db = database.mysql(self.database)
    api_key = self.test_api_key
    self.assertEqual(db.create_api_key(api_key, self.product, self.user), api_key)
    with self.assertRaises(Exception):  # This generated pymsql specifc error so I just check for an exception
      db.create_api_key(api_key,'api_keys','some_user')

    self.assertEqual(db.validate_api_key(api_key), self.product)
    self.assertEqual(db.delete_api_key(api_key), 0)

    with self.assertRaises(ValueError):
      db.delete_api_key(api_key)



if __name__ == '__main__':
  unittest.main()
