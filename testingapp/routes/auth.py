from testingapp import db, app, flask_bcrypt
from testingapp.models import User
from flask import request, jsonify
import jwt
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
       token = jwt.encode({'id' : user.id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=45)}, app.config['SECRET_KEY'], "HS256")
 
       return jsonify({'token' : token})
 
   return make_response('could not verify',  401, {'Authentication': '"login required"'})