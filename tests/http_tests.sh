url="$(curl ident.me -s):80/products"
echo "Using url ${url}"
echo "Testing GET"
response=$( curl -sL -w "%{http_code}\\n" ${url} -H "key:123_food" -o /dev/null ) 
echo "Getting food products"
if [[ ${response} == 200 ]]; then
  echo "Test passed!"
else
  echo "Test failed!"
  exit 1
fi
response=$( curl -sL -w "%{http_code}\\n" ${url} -H "key:123_textile" -o /dev/null ) 
echo "Getting textile products"
if [[ ${response} == 200 ]]; then
  echo "Test passed!"
else
  echo "Test failed!"
  exit 1
fi
echo "Testing POST"
response=$( curl -sL -w "%{http_code}\\n" ${url} -H 'Content-Type:application/json' -H 'key:123_food' -X PUT -d '{"name" : "some_name", "tags" : ["This", "hey"],"billOfMaterials": {"carrots": {"quantity" : 20, "unit" : "kg" }, "stuff": {"quantity" : 20, "unit" : "kg" }}, "family" : "fam", "customer": "cust", "allergens": ["allergen_1", "allergen_2"]  }' -o /dev/null )
echo "Adding food product"
if [[ ${response} == 201 ]]; then
  echo "Test passed!"
else
  echo "Test failed!"
  exit 1
fi
response=$( curl -sL -w "%{http_code}\\n" ${url} -H  'Content-Type:application/json' -H 'key:123_textile' -X PUT -d '{ "name" : "some_name", "tags" : ["This", "hey"],"billOfMaterials": {"carrots": {"quantity" : 20, "unit" : "kg" }, "stuff": {"quantity" : 20, "unit" : "kg" }}, "colour" : "nice", "range": "some_range"  }' -o /dev/null )
echo "Adding textile product"
if [[ ${response} == 201 ]]; then
  echo "Test passed!"
else
  echo "Test failed!"
  exit 1
fi
