import json
import dynamodb_handler as dynamodb #importing other personal script for DynamoDB operations
import random


GET_RAW_PATH = "/getrandomcookie"
CREATE_RAW_PATH = "/createcookie"

def lambda_handler(event, context):
    print (event)
    
    #Get RANDOM Cookie Functionality
    if event['rawPath'] == GET_RAW_PATH:
        print (f'Start Request for GET Cookie')
        total_cookies_count = dynamodb.itemCount() #getting count of all cookies in db
        print(f'Total cookies found is: {total_cookies_count} \n')
        random_number = random.randint(1, total_cookies_count ) #Generating random int from all entries
        print(f'Random number generated is: {random_number}')
        response = dynamodb.ReadFortunes(random_number)
        
        if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
            
            if ('Item' in response):
                return { 'Item': response['Item'] }
    
            return { 'msg' : 'Item not found!' }
    
        return {
            'msg': 'Some error occured',
            'response': response
        }
    
    #Create Cookie Functionality
    elif event['rawPath'] == CREATE_RAW_PATH:
        print (f'Start Request for CREATE Cookie')
        decodedevent = json.loads(event['body']) #decoding the incoming json item
        cookietext = decodedevent['text'] #extracting the text
        print(f'This is the cookie text: {cookietext}')

        # Find next available ID in table, it will write whatever text is incoming to next available table id
        total_cookies_count = dynamodb.itemCount() #getting count of all cookies in db
        print(f'Total cookies found is: {total_cookies_count} \n')

        next_available_id = total_cookies_count + 1
        print(f'Next available ID in table is: {next_available_id}')

        response = dynamodb.AddItemToFortunes(next_available_id, cookietext)
        print(f'This is the response after adding Cookie to db: ')
        print (response)    
        return response

    return {
            'msg': 'Some error occured',
            'response': response
        }



    