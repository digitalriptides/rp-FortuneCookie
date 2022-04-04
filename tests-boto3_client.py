import boto3
from flask import Flask, request, render_template
from decouple import config

AWS_ACCESS_KEY_ID     = config("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
REGION_NAME           = config("REGION_NAME")


# Client for lower level abstraction to AWS services
client = boto3.client(
    'dynamodb',
    aws_access_key_id     = AWS_ACCESS_KEY_ID,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
    region_name           = REGION_NAME,
)

# Resource is newer, higher level abstraction to AWS
resource = boto3.resource(
    'dynamodb',
    aws_access_key_id     = AWS_ACCESS_KEY_ID,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
    region_name           = REGION_NAME,
)

# In order to access and modify the entries of the table, 
# we have to get the table using the resource.
fortunestable = resource.Table('fortunesdb')

#test item to add
client_item = {
    "id": {"N": "20"},
    "text": {"S": "Quote #20."}
}

resource_item = {
    "id": 10,
    "text" : "This is test"
}

item_get = {
    "id": {"N": "1"}
}

if __name__ == '__main__':

    ### PUT ITEM
    #usint the Resource API
#    response = fortunestable.put_item(Item = resource_item)
#    print( response)

    #using the client
#    response = client.put_item(TableName='fortunesdb', Item = client_item)
#    print( response)

    ### GET ITEM
    response = client.get_item(TableName='fortunesdb', Key = item_get)


'''
    print('\n API RESPONSE: ')
    print(response)
    print('\n ITEM: ')
    print(response ['Item'])
    print('\n TEXT DICTIONARY: ')
    print(response ['Item']['text'])
    print('\n TEXT ONLY: ')
    print(response ['Item']['text']['S'])
'''