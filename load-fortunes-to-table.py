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
        TableName = 'fortune-cookies', # Name of the table 
        KeySchema = [       # Partition key/sort key attribute 
            {
                'AttributeName': 'id',
                'KeyType'      : 'HASH' 
                # 'HASH' -> partition key, 'RANGE' -> sort key
            }
        ],
        BillingMode = 'PAY_PER_REQUEST',
        )

# CreateATable() #Creates the table

fortune_cookies_table = resource.Table('fortune-cookies') #Uses the resource to select our table

def AddItemToFortunes(id, text):
    response = fortune_cookies_table.put_item(
        Item = {
            'id'     : int(id), #had to cast as integer for resource to take it
            'text'  : text
        }
    )
    print('Items added')    
    #return response

lines = []
count = 0


with open('smallsample-fortunes.txt') as f:
    lines = [line.rstrip() for line in f] # Removes the trailing new line characters
    print(f'This is the lines list: {lines}')
    print(len(lines))



for line in lines: # Loads the data
    count += 1
    AddItemToFortunes(count, line)
    print(f' Line {count}: {line}')

