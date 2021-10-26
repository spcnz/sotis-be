from testingapp import db, app, flask_bcrypt
from testingapp.models import User
from flask import request, jsonify
import jwt
from functools import wraps
import datetime

@app.route('/register', methods=['POST'])
def signup_user(): 
   data = request.get_json() 
 
   new_user = User(first_name=data['first_name'], last_name=data['last_name'], email=data['email'], password=data["password"])
   db.session.add(new_user) 
   db.session.commit()   

   return jsonify({'message': 'registered successfully'})


@app.route('/login', methods=['POST']) 
def login_user():
   auth = request.get_json() 
 
   user = User.query.filter_by(email=auth["email"]).first()  
   if (flask_bcrypt.check_password_hash(user.password_hash, auth["password"])):
        token = user.encode_auth_token()
        return jsonify({'token' : token.decode("utf-8")  })
 

