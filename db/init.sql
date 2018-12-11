CREATE DATABASE johannes_db;
use johannes_db;

CREATE TABLE product_types(
  Product_type VARCHAR(255) NOT NULL,
  PRIMARY KEY (Product_type)
);
CREATE TABLE api_keys(
  Api_key VARCHAR(255) NOT NULL,
  Product_type VARCHAR(255) NOT NULL,
  Userid VARCHAR(255) NOT NULL,
  PRIMARY KEY (api_key),
  FOREIGN KEY (Product_type) REFERENCES product_types(Product_type)
);
CREATE TABLE products(
  ID INT NOT NULL AUTO_INCREMENT,
  Name VARCHAR(255) NOT NULL,
  Product_type VARCHAR(255) NOT NULL,
  PRIMARY KEY (ID),
  FOREIGN KEY (Product_type) REFERENCES product_types(Product_type)
);
CREATE TABLE textile(
  ID INT NOT NULL,
  Colour VARCHAR(255),
  Prod_range VARCHAR(255),
  PRIMARY KEY(ID),
  FOREIGN KEY (ID) REFERENCES products(ID)
);
CREATE TABLE food(
  ID INT NOT NULL,
  Family VARCHAR(255),
  Customer VARCHAR(255),
  PRIMARY KEY(ID),
  FOREIGN KEY (ID) REFERENCES products(ID)
);
CREATE TABLE tags(
  Tag VARCHAR(255) NOT NULL,
  PRIMARY KEY(Tag)
);
CREATE TABLE allergens(
  Allergen VARCHAR(255) NOT NULL,
  PRIMARY KEY(Allergen)
);
CREATE TABLE materials(
  Material VARCHAR(255) NOT NULL,
  PRIMARY KEY(Material)
);
CREATE TABLE product_tags(
  ID INT NOT NULL,
  Tag VARCHAR(255) NOT NULL,
  PRIMARY KEY (ID, Tag),
  FOREIGN KEY (ID) REFERENCES products(ID),
  FOREIGN KEY (Tag) REFERENCES tags(Tag)
);
CREATE TABLE product_allergens(
  ID INT NOT NULL,
  Allergen VARCHAR(255) NOT NULL,
  PRIMARY KEY (ID, Allergen),
  FOREIGN KEY (ID) REFERENCES products(ID),
  FOREIGN KEY (Allergen) REFERENCES allergens(Allergen)
);
CREATE TABLE product_materials(
  ID INT NOT NULL,
  Material VARCHAR(255) NOT NULL,
  Quantity DOUBLE(255, 1),
  Unit VARCHAR(255),
  PRIMARY KEY (ID, Material),
  FOREIGN KEY (Material) REFERENCES materials(Material),
  FOREIGN KEY (ID) REFERENCES products(ID)
);

INSERT INTO product_types VALUES('textile');
INSERT INTO product_types VALUES('food');
INSERT INTO api_keys (Api_key, Product_type, Userid) VALUES ('123', 'food','jesbjorn');

