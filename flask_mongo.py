import json
import os,time
from flask import Flask, request, jsonify , flash,redirect 
from flask_mongoengine import MongoEngine
from datetime import date
import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)


DB_URI = "mongodb+srv://Udhay_16:Udhaymongodb@cluster0.yxx4q.mongodb.net/usermanagement?retryWrites=true&w=majority"

app.config["MONGODB_HOST"] = DB_URI

db = MongoEngine(app)

UPLOAD_FOLDER = 'profile_images' #File save folder

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#User Model
class User(db.Document):
    username = db.StringField()
    password = db.StringField()
    email = db.StringField()
    mobile_no = db.IntField()
    profile_image = db.StringField()
    created_at = db.DateTimeField(default=datetime.datetime.now)
    updated_at = db.DateTimeField()
    status = db.IntField()


    def to_json(self):
        return {"username": self.username,
                "password":self.password,
                "email": self.email,
                 "mobile_no":self.mobile_no,
                 "profile_image":self.profile_image,
                 "created_at":self.created_at,
                 "updated_at":self.updated_at

                }


@app.route('/', methods=['GET'])
def users():

    """Get the user details for using this function

    Arguments
    ---------
    page
        pagination page number

    limit
        how many records showed per page

    Returns
    -------
    json
        a status of function return json format
    """
    
    page  = int(request.args.get('page',1))
    limit = int(request.args.get('limit',5))
    
    users = User.objects(status=1).paginate(page=page,per_page=limit)
    if not users:
        return jsonify({'error': 'data not found'})
    else:
        return jsonify([u.to_json() for u in users.items])


#Create User
@app.route('/user', methods=['POST'])
def create_user():

    """Create the user for using this function

    Returns
    -------
    json
        a status of function return json format
    """
    
    user = request.form #user form
    #check file upload or not
    if 'file' not in request.files:
        return jsonify({'status': 'failed','error':"File Not Found"})

    #File upload into folder   
    file = request.files['file']
    filename = secure_filename(file.filename)
    
    filename = str(int(time.time())) + "_" + filename
    file_folder = file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    profile_image = UPLOAD_FOLDER + "/" + filename 
    
    created_at = datetime.datetime.now()
    
    

    user = User(username=user['username'],
                email=user['email'],
                password = user['password'],
                mobile_no=user['mobile_no'],
                profile_image=profile_image,
                created_at=created_at,
                status=1)
    user.save()
    #return jsonify(user.to_json())
    return jsonify({'status': 'success','messgage':'User created Successfully!.'})
    

@app.route('/user', methods=['PUT'])
def update_user():

    """Update the user for using this function

    Returns
    -------
    json
        a status of function return json format
    """
    
    user = request.form
    
    if 'username' not in user:
        return jsonify({'error':"Username is must to Edit the data!."})

    record = User.objects(username=user['username']).first()

    if not record:
        return jsonify({'status': 'failed','error': 'user not found'})
    else:
        #File upload into folder
        if request.files:
            
            profile_image = record.profile_image
            
            os.unlink(profile_image) #unlink previous file
            
            file = request.files['file']
            filename = secure_filename(file.filename)
            filename = str(int(time.time())) + "_" + filename
            file_folder = file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            profile_image = UPLOAD_FOLDER+"/"+  filename
        
        record.update(profile_image=profile_image, updated_at=datetime.datetime.now(), **user)
        record = User.objects(username=user['username']).first()
    
    return jsonify({'status': 'success','messgage':'User data Updated Successfully!.'})


@app.route('/user', methods=['DELETE'])
def delete_user():
    """Deleting the user for using this function

    Returns
    -------
    json
        a status of function return json format
    """

    
    user =request.form

    if 'username' not in user:
        return jsonify({'error':"Username is Must to Delete the data!."})

    user = User.objects(username=user['username']).first()
    if not user:
        return jsonify({'status': 'failed','error': 'data not found'})
    else:
        user.update(status=2)
    return jsonify({'status':'success',"message":"User Deleted Successfully!."})

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=8000)
