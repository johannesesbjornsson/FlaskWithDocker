import sqlalchemy as db
import os

from sqlalchemy import event

class mysql(object):

  def __init__(self,database='db'):
    database = os.environ['DATABASE']  # Getting the envrionmetal var (db for production)
    self.engine = db.create_engine('mysql+pymysql://root:root@'+database+':3306/johannes_db',pool_size=20,pool_recycle=3600)
    self.metadata = db.MetaData(bind=None)

  def create_product(self,name,product_type,product_data):  # Takes product data as a dict with tables names as keys and columns as values
    conn = self.engine.connect()
    prod = db.Table('products', self.metadata, autoload = True, autoload_with = self.engine)
    new_prod= prod.insert().values(Name=name,Product_type=product_type)
    trans = conn.begin()  # Beginning a sqlalchemy transation
    try:
      prod_id = conn.execute(new_prod).inserted_primary_key[0]  # Gets the primary key that was generated from the product table
      for table_name in product_data:  # Loops through the tables that are going to have values inserted
        for index in range(len(product_data[table_name])):  #  Loops through the values in the the product_data argument that was passed
          if 'ID' in product_data[table_name][index]:  # Checks for the id column
            product_data[table_name][index]['ID'] = prod_id  # Replaces the current ID value '' to the one created by the product table
        table = db.Table(table_name, self.metadata, autoload = True, autoload_with = self.engine)  # Create table object
        conn.execute(table.insert(),product_data[table_name])  # Inserts the values passed with the update ID value
      trans.commit()  # Commits all changes to database
    except:
      trans.rollback()  # Undo all changes to the database since trans.begin()
      raise  # Raises the some error that was caught
    conn.close()
    return 0

  def get_products(self,product_type,tables):  # takes prouct type and any tables containing data on that prouct
    conn = self.engine.connect()
    products = db.Table('products', self.metadata, autoload = True, autoload_with = self.engine)
    stmt = db.select([products]).where(products.c.Product_type == product_type)  # Getting name and id from product table
    products_of_type= conn.execute(stmt).fetchall()
    product_list = []
    for product in products_of_type:  # Iterates throug all the returned products
      data = {}
      data['id'] = product.ID
      data['name'] = product.Name
      product_specific_data = self.get_poduct_specific_data(product_type,product.ID,conn)  
      data.update(product_specific_data)
      for table_name in tables:  # Iterates through any two column column tables containing data on this prouct
        associated_data = self.get_product_associated_data(table_name,product.ID,conn)
        data[table_name] = associated_data
      product_list.append(data)  # Adding all data of specfic product to list
    conn.close()
    return product_list  # Returning a list of dictionaries(each one being a product)

  def get_product_associated_data(self,table_name,product_id,conn):  # Get data from any table containing only two columns (one being the prodcut id)
    table = db.Table(table_name, self.metadata, autoload = True, autoload_with = self.engine)
    stmt = db.select([table]).where(table.c.ID == product_id)
    product_data = conn.execute(stmt)
    if product_data.rowcount < 1:
      return None
    columns =product_data.keys()
    keys = [str(x.lower()) for x in columns]  # Converting column names(starting with captial letter) to lowercase

    rows = product_data.fetchall()
    product_info = []
    for row in rows:
      product_specfic_data = dictionary = dict(zip(keys, row))  # Creating dictionary from column names(as keys) and column values returned
      product_specfic_data.pop('id')  # Remoing id since that information is already known
      product_info.append(product_specfic_data)  # adding to list in format {'cloumn_name': 'column_value'}
    return product_info  # returns list of single valued dictionaries

  def get_poduct_specific_data(self,product_type,product_id,conn):  # Based on table name and pruct ID product specifc data is fetched
    product_specific = db.Table(product_type, self.metadata, autoload = True, autoload_with = self.engine)
    stmt = db.select([product_specific]).where(product_specific.c.ID == product_id)  
    product_data = conn.execute(stmt)
    columns =product_data.keys()
    keys = [str(x.lower()) for x in columns]  # Converting column names(starting with captial letter) to lowercase
    row = product_data.fetchone()
    if row is None:
      return {}
    product_specfic_data = dictionary = dict(zip(keys, row))  # Creating dictionary from column names(as keys) and column values returned
    product_specfic_data.pop('id')  # Remoing id since that information is already known 
    return product_specfic_data 
      
  def create_api_key(self,key,product,user):
    conn = self.engine.connect()
    table = db.Table('api_keys', self.metadata, autoload = True, autoload_with = self.engine)
    new_key = table.insert().values(Api_key=key,Product_type=product,Userid=user)
    res = conn.execute(new_key)
    conn.close()
    return 0

  def delete_api_key(self,key):
    conn = self.engine.connect()
    table = db.Table('api_keys', self.metadata, autoload = True, autoload_with = self.engine)
    stmt = table.delete(table.c.Api_key == key)
    res = conn.execute(stmt)
    if res.rowcount < 1:
      raise ValueError("API key not found")
    conn.close()
    return 0

  def validate_api_key(self,key):
    conn = self.engine.connect()
    table = db.Table('api_keys', self.metadata, autoload = True, autoload_with = self.engine)
    stmt = db.select([table.c.Product_type]).where(table.c.Api_key == key)
    prod = conn.execute(stmt).fetchone()
    if not prod:
      raise ValueError("Invalid API Key")
    conn.close()
    return prod[0]

  def get_tags(self,tags):
    conn = self.engine.connect()
    table = db.Table('tags', self.metadata, autoload = True, autoload_with = self.engine)
    stmt = db.select([table.c.Tag]).where(table.c.Tag.in_(tags))
    found_tags = conn.execute(stmt).fetchall()
    conn.close()
    return found_tags

  def delete_tags(self,tags):
    conn = self.engine.connect()
    table = db.Table('tags', self.metadata, autoload = True, autoload_with = self.engine)
    stmt = table.delete(table.c.Tag.in_(tags))
    res = conn.execute(stmt)
    if res.rowcount < 1:
      raise ValueError("No tags found")
    conn.close()
    return 0

  def get_allergens(self,allergens):
    conn = self.engine.connect()
    table = db.Table('allergens', self.metadata, autoload = True, autoload_with = self.engine)
    stmt = db.select([table.c.Allergen]).where(table.c.Allergen.in_(allergens))
    found_allergens = conn.execute(stmt).fetchall()
    conn.close()
    return found_allergens

  def delete_allergens(self,allergens):
    conn = self.engine.connect()
    table = db.Table('allergens', self.metadata, autoload = True, autoload_with = self.engine)
    stmt = table.delete(table.c.Allergen.in_(allergens))
    res = conn.execute(stmt)
    if res.rowcount < 1:
      raise ValueError("No allergens found")
    conn.close()
    return 0

  def get_materials(self,materials):
    conn = self.engine.connect()
    table = db.Table('materials', self.metadata, autoload = True, autoload_with = self.engine)
    stmt = db.select([table.c.Material]).where(table.c.Material.in_(materials))
    found_materials = conn.execute(stmt).fetchall()
    conn.close()
    return found_materials

  def delete_materials(self,materials):
    conn = self.engine.connect()
    table = db.Table('materials', self.metadata, autoload = True, autoload_with = self.engine)
    stmt = table.delete(table.c.Material.in_(materials))
    res = conn.execute(stmt)
    if res.rowcount < 1:
      raise ValueError("No materials found")
    conn.close()
    return 0

  def add_to_single_column_table(self,table_name,values):  # generic insert function for any single columned table
    conn = self.engine.connect()
    table = db.Table(table_name, self.metadata, autoload = True, autoload_with = self.engine)
    ins = table.insert()
    conn.execute(ins,values)
    conn.close()
    return 0
