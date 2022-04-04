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

### SPECIFIC ID COOKIE
@app.route('/<int:id>', methods=['GET']) 
def getCookie(id):
    response = dynamodb.ReadFortunes(id)
        
    if (response['ResponseMetadata']['HTTPStatusCode'] == 200):        
        if ('Item' in response):
            print(response)
            cookie_id = response['Item']['id']
            print(f'This is the cookie ID: {cookie_id} \n')

            cookie_text = response['Item']['text']
            return render_template('singlecookie.html', cookie_text = cookie_text, cookie_id=cookie_id)
            # return { 'Item': response['Item'] }

        return { 'msg' : 'Item not found!' }

    return {
        'msg': 'Some error occured',
        'response': response
    }
    return render_template('post.html', post=post)

### ADD A COOKIE
@app.route('/addcookie', methods=('GET', 'POST'))
def create():

    if request.method == 'GET':
        return render_template('addcookie.html')

    elif request.method == 'POST':
        cookie_text = request.form['cookie_text']
        cookie_id = int(request.form['cookie_id'])

        
        response = dynamodb.AddItemToFortunes(cookie_id, cookie_text)    
        
        if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
            flash('Your Cookie was successfully added!','info')
            return redirect(url_for('index'))

        return {  
            'msg': 'Some error occcured',
            'response': response
        }


### EDIT A COOKIE
@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def editCookie(id):
    response = dynamodb.ReadFortunes(id)
    cookie_text = response['Item']['text']
    cookie_id = response['Item']['id']

    if request.method == 'POST':
        cookie_text = request.form['cookie_text']
        cookie_id = request.form['cookie_id']
        response = dynamodb.UpdateFortune(cookie_id, cookie_text)

        if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
            flash('Cookie Successfully Edited!','info')
            return redirect(url_for('index'))

        return {  
            'msg': 'Some error occcured',
            'response': response
        }   
       
    return render_template('editcookie.html', cookie_text = cookie_text, cookie_id=cookie_id) 

#  Update a fortune entry
#  Route: http://localhost:5000/update/fortune/<id>
#  Method : PUT
@app.route('/update/fortune/<int:id>', methods=['GET','PUT'])
def UpdateFortune(id):

    data = request.get_json()
    

    # this is grabbing the incoming requests data, the data is a dict
    # data = {
    #     'text': "fortune_text"
    # }

    response = dynamodb.UpdateFortune(id, data)

    if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
        return {
            'msg'                : 'Updated successfully',
            'ModifiedAttributes' : response['Attributes'],
            'response'           : response['ResponseMetadata']
        }

    return {
        'msg'      : 'Some error occured',
        'response' : response
    }   


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)