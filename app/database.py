import sqlalchemy as db
import pymysql.err
class mysql(object):

  def __init__(self,database='db'):
    self.engine = db.create_engine('mysql+pymysql://root:root@'+database+':3306/products',pool_size=20,pool_recycle=3600)

  def create_api_key(self,key,product,user):
    conn = self.engine.connect()
    tables = self.engine.table_names()
    if not product.lower() in tables:
      raise NameError("Specifced product does not exist")

    metadata = db.MetaData(bind=None)
    table = db.Table('api_keys', metadata, autoload = True, autoload_with = self.engine)
    ins = table.insert()
    new_key = ins.values(api_key=key,product=product,userid=user)
    res = conn.execute(new_key)
    conn.close()
    return key

  def delete_api_key(self,key):
    conn = self.engine.connect()
    metadata = db.MetaData(bind=None)
    table = db.Table('api_keys', metadata, autoload = True, autoload_with = self.engine)
    stmt = table.delete(table.c.api_key == key)
    res =conn.execute(stmt)
    if res.rowcount < 1:
      raise ValueError("API key not found")
    conn.close()
    return 0

  def validate_api_key(self,key):
    conn = self.engine.connect()
    metadata = db.MetaData(bind=None)
    table = db.Table('api_keys', metadata, autoload = True, autoload_with = self.engine)
    stmt = db.select([table.c.product]).where(table.c.api_key == key)
    key = conn.execute(stmt).fetchone()
    if not key:
      raise ValueError("Invalid API Key")
    conn.close()
    return key.product


