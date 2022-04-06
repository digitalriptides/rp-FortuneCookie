from audioop import findfactor
from flask import Flask, request, render_template, jsonify, flash, redirect, url_for
import dynamodb_handler as dynamodb #importing other personal script for DynamoDB operations
from decouple import config
import random

FLASK_SECRET_KEY     = config("FLASK_SECRET_KEY")

app = Flask(__name__)

app.secret_key = FLASK_SECRET_KEY 

### INDEX
@app.route("/")
def index():
    return render_template("index.html")
 
 ### RANDOM
@app.route('/random', methods=['GET'])
def getRandomcookie():
    total_cookies_count = dynamodb.itemCount() #getting count of all cookies in db
    print(f'Total cookies found is: {total_cookies_count} \n')
    random_number = random.randint(1, total_cookies_count ) #Generating random int from all entries
    print(f'Random number generated is: {random_number}')
    response = dynamodb.ReadFortunes(random_number)

    if (response['ResponseMetadata']['HTTPStatusCode'] == 200):        
        if ('Item' in response):
            print(response)
            cookie_id = response['Item']['id']
            print(f'This is the cookie ID: {cookie_id} \n')

            cookie_text = response['Item']['text']
            return render_template('cookie.html', cookie_text = cookie_text, cookie_id=cookie_id)
            # return { 'Item': response['Item'] }

        return { 'msg' : 'Item not found!' }

    return {
        'msg': 'Some error occured',
        'response': response
    }


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)