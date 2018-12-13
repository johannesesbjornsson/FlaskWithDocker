INSTALLING  
UBUNTU  
on a virtual machine with http traffic enabled  
sudo apt-get update  
sudo apt-get install python-dev python-pip git docker.io  
docker --version  

sudo curl -L https://github.com/docker/compose/releases/download/1.21.2/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose  
sudo chmod +x /usr/local/bin/docker-compose  
docker-compose --version  
docker version 18.06.1-ce  
docker-compose version 1.21.2  


START  
sudo docker-compose build  
sudo docker-compose up
sudo docker-compose start  

TESTS   
sudo docker-compose -f docker-compose.test.yml build  
  
Adding food products: curl http://{id-address}:80/products -H 'Content-Type:application/json' -H 'key:123_food' -X PUT -d '{ "name" : "some_name", "tags" : ["This", "hey"],"billOfMaterials": {"carrots": {"quantity" : 20, "unit" : "kg" }, "stuff": {"quantity" : 20, "unit" : "kg" }}, "family" : "fam", "customer": "cust", "allergens": ["allergen_1", "allergen_2"]  }'  
  
Adding textile products: curl http://{id-address}:80/products -H 'Content-Type:application/json' -H 'key:123_textile' -X PUT -d '{ "name" : "some_name", "tags" : ["This", "hey"],"billOfMaterials": {"carrots": {"quantity" : 20, "unit" : "kg" }, "stuff": {"quantity" : 20, "unit" : "kg" }}, "colour" : "nice", "range": "some_range"  }'  
  
getting textile products: http://{id-address}:80/products -H 'key:123_textile'  
getting food products: http://{id-address}:80/products -H 'key:123_textile'  

  
Steps I would take to make this production ready would be to add delete product functionality, more tests(specifially testing badly formatted requests), paging functionality, adding better error handling. Most errors are just handledd as generic Excpetions and doesn't give much insight in what acutally went wrong. Paging functionaly in the api response, such as only displaying 25-100 products per api call (determined by an offset argument) and proving number of pages as part of the response. By default you have landed on page1, but in the GET request you would have the ability to display specific page. My current solution wouldn't scale well in that regard, as responses would become too large when the number of products would hit the hundreds. The reason I have not done all this is because of time constraints

  
Assumptions:
Since the specification says that the product you have access to is determined soley on the API key, I assume that there won't be users that have access to mutiple. With my solution it would therefore require a bit of work to add admin or other more privileged users  
