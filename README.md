### Requirements: ###
docker  
docker-compose  
port 3306 free  

### Installation guides:  ###
Docker (Ubuntu): https://docs.docker.com/install/linux/docker-ce/ubuntu/  
Docker (Debian): https://docs.docker.com/install/linux/docker-ce/debian/  
Docker compose (Both): https://docs.docker.com/compose/install/  
  
Confirmed working on Ubuntu 18.04 LTS (Docker version 18.06.1-ce and docker-compose version 1.21.2)  
Confirmed working on Dembian 9 (Docker version 18.09.0, docker-compose version 1.23.1)
  
### Get the code up and running ###
git clone https://github.com/johannesesbjornsson/FlaskWithDocker.git  
cd FlaskWithDocker

#### START #### 
sudo docker-compose build  
sudo docker-compose up
sudo docker-compose start  

#### TESTS ####  
sudo docker-compose -f docker-compose.test.yml build  
  
### Accessing the API ###  
Adding food products: curl http://{id-address}:80/products -H 'Content-Type:application/json' -H 'key:123_food' -X PUT -d '{ "name" : "some_name", "tags" : ["This", "hey"],"billOfMaterials": {"carrots": {"quantity" : 20, "unit" : "kg" }, "stuff": {"quantity" : 20, "unit" : "kg" }}, "family" : "fam", "customer": "cust", "allergens": ["allergen_1", "allergen_2"]  }'  
  
Adding textile products: curl http://{id-address}:80/products -H 'Content-Type:application/json' -H 'key:123_textile' -X PUT -d '{ "name" : "some_name", "tags" : ["This", "hey"],"billOfMaterials": {"carrots": {"quantity" : 20, "unit" : "kg" }, "stuff": {"quantity" : 20, "unit" : "kg" }}, "colour" : "nice", "range": "some_range"  }'  
  
getting textile products: http://{id-address}:80/products -H 'key:123_textile'  
getting food products: http://{id-address}:80/products -H 'key:123_textile'  

### Making the code production ready ### 
Steps I would take to make this production ready would be to add delete product functionality, more tests(specifially testing badly formatted requests), paging functionality and adding better error handling. Most errors are just handledd as generic Excpetions and doesn't give much insight in what acutally went wrong. Paging functionaly in the api response, such as only displaying 25-100 products per api call (determined by an offset argument) and proving number of pages as part of the response. By default you have landed on page1, but in the GET request you would have the ability to display specific page. My current solution wouldn't scale well in that regard, as responses would become too large when the number of products would hit the hundreds. The reason I have not done all this is because of time constraints
  
### Assumptions ###
Since the specification says that the product you have access to is determined soley on the API key, I assume that there won't be users that have access to mutiple. With my solution it would therefore require a bit of work to add admin or other more privileged users  
