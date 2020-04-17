from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS
import random
import string


app = Flask(__name__)
CORS(app)

users = { 
   'users_list' :
   [
      { 
         'id' : 'xyz789',
         'name' : 'Charlie',
         'job': 'Janitor',
      },
      {
         'id' : 'abc123', 
         'name': 'Mac',
         'job': 'Bouncer',
      },
      {
         'id' : 'ppp222', 
         'name': 'Mac',
         'job': 'Professor',
      }, 
      {
         'id' : 'yat999', 
         'name': 'Dee',
         'job': 'Aspring actress',
      },
      {
         'id' : 'zap555', 
         'name': 'Dennis',
         'job': 'Bartender',
      }
   ]
}

def genRandomId(stringLength=5):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(stringLength))

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/users/<id>')
def get_user(id):
   if id :
      for user in users['users_list']:
        if user['id'] == id:
           return user
      return ({})
   return users

@app.route('/users', methods=['GET', 'POST'])
def get_users():
   if request.method == 'GET':
      search_username = request.args.get('name')
      job = request.args.get('job')
      
      if search_username :
         subdict = {'users_list' : []}
         for user in users['users_list']:
            if user['name'] == search_username:
               if not job:
                  subdict['users_list'].append(user)
               elif user['job'] == job:
                  subdict['users_list'].append(user)


         return subdict
      return users
   elif request.method == 'POST':
      userToAdd = request.get_json()
      userToAdd["id"] = genRandomId()
      users['users_list'].append(userToAdd)
      resp = jsonify(success=True, data = userToAdd)
      resp.status_code = 201
      #resp.status_code = 200 #optionally, you can always set a response code. 
      # 200 is the default code for a normal response
      return resp

@app.route('/users/<string:userID>', methods=["DELETE"])
def deleteUser(userID):
   if request.method == 'DELETE':
      resp = jsonify(success=False)
      resp.status_code = 400
      for ind,user in enumerate(users['users_list']):
         if user["id"] == userID:
            users['users_list'].pop(ind)
            resp.status_code = 200
            resp = jsonify(success=True, userID=userID)

      return resp

