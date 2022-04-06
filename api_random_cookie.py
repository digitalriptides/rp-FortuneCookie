from audioop import findfactor
from flask import Flask, request, render_template, jsonify, flash, redirect, url_for
import dynamodb_handler as dynamodb #importing other personal script for DynamoDB operations
from decouple import config
import random
import requests 
import json

FLASK_SECRET_KEY     = config("FLASK_SECRET_KEY")

app = Flask(__name__)

app.secret_key = FLASK_SECRET_KEY 

### INDEX
@app.route("/")
def index():
    return render_template("index.html")
 
 ### Get Random Cookie from API / DynamoDB
@app.route('/random', methods=['GET'])
def getRandomcookie():

    response = requests.get(
            "https://cookieapi.digitalriptides.com/getrandomcookie"
       )
    decoded_response = response.json()
    print(decoded_response)
            
    if ('Item' in decoded_response):
        
        cookie_id = decoded_response['Item']['id']
        print(f'This is the cookie ID: {cookie_id} \n')

        cookie_text = decoded_response['Item']['text']
        return render_template('api_random_cookie.html', cookie_text = cookie_text, cookie_id=cookie_id)
        # return { 'Item': response['Item'] }

    return {
        'msg': 'Some error occured',
        'response': decoded_response
    }


### CREATE A COOKIE VIA API 
@app.route('/createcookie', methods=('GET', 'POST'))
def create():

    if request.method == 'GET':
        return render_template('api_createcookie.html')

    elif request.method == 'POST':
        #Cookie ID not being used, random selected in lambda
        cookie_text = request.form['cookie_text'] 
        #cookie_id = int(request.form['cookie_id'])

        
        response = requests.post(
            "https://cookieapi.digitalriptides.com/createcookie", json= {"id": "200", "text": cookie_text } 
       )
        
        print(f"Status Code: {response.status_code}, Response: {response.json()}")
        flash('Your Cookie was successfully added!','info')
        return redirect(url_for('index'))
        


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)