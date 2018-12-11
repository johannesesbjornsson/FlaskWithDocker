import sqlalchemy as db
import os

from sqlalchemy import event

class mysql(object):

  def __init__(self,database='db'):
    database = os.environ['DATABASE']
    self.engine = db.create_engine('mysql+pymysql://root:root@'+database+':3306/johannes_db',pool_size=20,pool_recycle=3600)
    self.metadata = db.MetaData(bind=None)

  def create_product(self,name,product_type,product_data):  # Takes product data as a dict with tables names as keys and columns as values
    conn = self.engine.connect()
    prod = db.Table('products', self.metadata, autoload = True, autoload_with = self.engine)
    new_prod= prod.insert().values(Name=name,Product_type=product_type)
    trans = conn.begin()
    try:
      prod_id = conn.execute(new_prod).inserted_primary_key[0]
      for table_name in product_data:
        for index in range(len(product_data[table_name])):
          if 'ID' in product_data[table_name][index]:
            product_data[table_name][index]['ID'] = prod_id
        table = db.Table(table_name, self.metadata, autoload = True, autoload_with = self.engine)
        conn.execute(table.insert(),product_data[table_name])
      trans.commit()
    except:
      trans.rollback()
      raise
    
    conn.close()
    return 0

  def get_products(self,product_type,tables):
    conn = self.engine.connect()
    products = db.Table('products', self.metadata, autoload = True, autoload_with = self.engine)
    stmt = db.select([products]).where(products.c.Product_type == product_type)
    products_of_type= conn.execute(stmt).fetchall()
    product_list = []
    for product in products_of_type:
      data = {}
      data['id'] = product.ID
      data['name'] = product.Name
      product_specific_data = self.get_poduct_specific_data(product_type,product.ID,conn)
      data.update(product_specific_data)
      for table_name in tables:
        associated_data = self.get_product_associated_data(table_name,product.ID,conn)
        data[table_name] = associated_data
      product_list.append(data)
    conn.close()
    return product_list

  def get_product_associated_data(self,table_name,product_id,conn):
    table = db.Table(table_name, self.metadata, autoload = True, autoload_with = self.engine)
    stmt = db.select([table]).where(table.c.ID == product_id)
    product_data = conn.execute(stmt)
    if product_data.rowcount < 1:
      return None
    columns =product_data.keys()
    keys = [str(x.lower()) for x in columns]

    rows = product_data.fetchall()
    product_info = []
    for row in rows:
      product_specfic_data = dictionary = dict(zip(keys, row))
      product_specfic_data.pop('id') 
      product_info.append(product_specfic_data)
    return product_info

  def get_poduct_specific_data(self,product_type,product_id,conn):
    product_specific = db.Table(product_type, self.metadata, autoload = True, autoload_with = self.engine)
    stmt = db.select([product_specific]).where(product_specific.c.ID == product_id)
    product_data = conn.execute(stmt)
    columns =product_data.keys()
    keys = [str(x.lower()) for x in columns]
    row = product_data.fetchone()
    if row is None:
      return {}
    product_specfic_data = dictionary = dict(zip(keys, row))
    product_specfic_data.pop('id') 
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

  def add_to_single_column_table(self,table_name,values):  
    conn = self.engine.connect()
    table = db.Table(table_name, self.metadata, autoload = True, autoload_with = self.engine)
    ins = table.insert()
    conn.execute(ins,values)
    conn.close()
    return 0
