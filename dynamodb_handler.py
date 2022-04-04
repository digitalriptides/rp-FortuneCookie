import boto3
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


def CreateATable():
    client.create_table(
        AttributeDefinitions = [ # Name and type of the attributes 
            {
                'AttributeName': 'id', # Name of the attribute
                'AttributeType': 'N'   # N -> Number (S -> String, B-> Binary)
            }
        ],
        TableName = 'fortunesdb', # Name of the table 
        KeySchema = [       # Partition key/sort key attribute 
            {
                'AttributeName': 'id',
                'KeyType'      : 'HASH' 
                # 'HASH' -> partition key, 'RANGE' -> sort key
            }
        ],
        BillingMode = 'PAY_PER_REQUEST',
        Tags = [ # OPTIONAL 
            {
                'Project': 'dynamodb-test'
            }
        ]
        )

    
# In order to access and modify the entries of the table, 
# we have to get the table using the resource API
fortunestable = resource.Table('fortunesdb')

#Counting Rows in table to find total number of cookies found
def itemCount():
    all_items_count = fortunestable.item_count
    return all_items_count

#create a new fortune in the table
def AddItemToFortunes(id, text):
    response = fortunestable.put_item(
        Item = {
            'id'     : int(id), #had to cast as integer for resource to take it
            'text'  : text
        }
    )    
    return response

#Read a fortune in the table
def ReadFortunes(id):
    response = fortunestable.get_item(
        Key = {
            'id'     : id
        },
    AttributesToGet=[ #this is read-handler-return-id branch, working on branch
        'text',
        'id'
        ]
    )    
    return response


def UpdateFortune(id, data:dict):
    response = fortunestable.update_item(
        Key = {
            'id': int(id)
        },
        AttributeUpdates={
            'text': {
                'Value'  : data,
                'Action' : 'PUT' # available options -> DELETE(delete), PUT(set), ADD(increment)
            }
        },
        ReturnValues = "UPDATED_NEW" # returns the new updated values
    )    
    return response

def DeleteFortune(id):
    response = fortunestable.delete_item(
        Key = {
            'id': id
        }
    )   
    return response