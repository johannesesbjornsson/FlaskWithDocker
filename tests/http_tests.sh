url="$(curl ident.me -s):80/products"

echo "Testing GET"
response=$( curl -sL -w "%{http_code}\\n" ${url} -H "key:123" -o /dev/null ) 
if [[ ${response} == 200 ]]; then
  echo "Test passed"
  exit 0
else
  echo "Test failed!"
  exit 1
fi
