import json
import dynamodb_handler as dynamodb #importing other personal script for DynamoDB operations


GET_RAW_PATH = "/getcookie"
CREATE_RAW_PATH = "/createcookie"

def lambda_handler(event, context):
    print (event)
    
    #Get Cookie Functionality
    if event['rawPath'] == GET_RAW_PATH:
        print (f'Start Request for GET Cookie')
        cookieid = event['queryStringParameters']['id']
        print(f'Request received with cookie id = ' + cookieid)

        
        response = dynamodb.ReadFortunes(cookieid)
        
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



    