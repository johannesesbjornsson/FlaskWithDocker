url="$(curl ident.me -s):80/products"
response=$( curl -sL -w "%{http_code}\\n" ${url} -H "key:123" -o /dev/null ) 

if [[ ${response} == 200 ]]; then
  echo "Tests passed!"
  exit 0
else
  echo "Tests failed!"
  exit 1
fi
