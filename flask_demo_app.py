from flask import Flask, request, render_template, jsonify 
import dynamodb_handler as dynamodb #importing other script with functions
import random


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

###Create original table
#  Route: http://localhost:5000/createtable
@app.route('/createtable')
def root_route():
    dynamodb.CreateATable()
    return 'Created Table'

#  Add a Fortune
#  Route: http://localhost:5000/addfortune
#  Method : POST
@app.route('/addfortune', methods=['GET','POST'])
def addAFortune():

    data = request.get_json()
    # {"id":"15", "text": "this is text from postman 15"}
    # data

    response = dynamodb.AddItemToFortunes(data['id'], data['text'])    
    
    if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
        return {
            'msg': 'Added successfully',
        }

    return {  
        'msg': 'Some error occcured',
        'response': response
    }

#  Read a Fortune
#  Route: http://localhost:5000/fortune/<id>
#  Method : GET
@app.route('/fortune/<int:id>', methods=['GET'])
def getFortune(id):
    response = dynamodb.ReadFortunes(id)
    
    if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
        
        if ('Item' in response):
            return { 'Item': response['Item'] }

        return { 'msg' : 'Item not found!' }

    return {
        'msg': 'Some error occured',
        'response': response
    }

#  Read a Random Fortune
#  Route: http://localhost:5000/random
#  Method : GET
@app.route('/random', methods=['GET'])
def getRandomFortune():
    random_number = random.randint(1, 6)
    print(f'Random fortune ID is: {random_number}')

    response = dynamodb.ReadFortunes(random_number)
    
    if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
        
        if ('Item' in response):
            
            print(f'This is the response: {response}')
            randomtext = response['Item']['text']
            finaltext = randomtext.capitalize()
            return render_template("index.html", dynamicfortune=finaltext)
             
        return { 'msg' : 'Item not found!' }

    return {
        'msg': 'Some error occured',
        'response': response
    }


#  Delete a Fortune
#  Route: http://localhost:5000/delete/fortune/<id>
#  Method : DELETE
@app.route('/delete/fortune/<int:id>', methods=['GET','DELETE'])
def DeleteAFortune(id):

    response = dynamodb.DeleteFortune(id)

    if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
        return {
            'msg': 'Deleted successfully',
        }

    return {  
        'msg': 'Some error occcured',
        'response': response
    } 


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
