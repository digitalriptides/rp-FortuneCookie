import requests

# proper syntax on sending json from a Python client:
# response = requests.post('http://localhost:5000/api/add_message/1234', json={"mytext":"lalala"})

response = requests.put('http://localhost:5000/update/fortune/1', json={'id':'1', 'text':'Updating text with manual request'})
print(response.json())
