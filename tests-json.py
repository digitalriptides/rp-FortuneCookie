import json

# json_item = r'''{"body":"{\r\n    \"id\" : \"5\"\r\n    \"text\" : \"POSTING: this is the text to add\"\r\n}"}'''
'''
decodedItem = json.loads(json_item)
print (f'this is the item: {json_item}')
print('\n')
print (f'this is the item: ')
print(decodedItem['body'][0])
'''

json_item = '''{"body":"{\r\n    \"id\" : \"5\"\r\n    \"text\" : \"POSTING: this is the text to add\"\r\n}"}'''

new_item = json_item.replace('\\', '\\')


print(f'text here: {new_item}')
