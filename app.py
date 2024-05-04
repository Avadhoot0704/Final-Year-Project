from __future__ import division, print_function
import sys
import os
import glob
import re
import numpy as np


from keras.applications.imagenet_utils import preprocess_input, decode_predictions
from keras.models import load_model
from keras.preprocessing import image


from flask import Flask, redirect, url_for, request, render_template, session
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer
from flask import Flask
from flask_sqlalchemy import SQLAlchemy




app = Flask(__name__)
app.secret_key = '123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Aaudut%40123@localhost/pneumonia'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    age = db.Column(db.String(20))
    phn_number = db.Column(db.String(20))
    result = db.Column(db.String(20))

with app.app_context():
    db.create_all()

MODEL_PATH = 'models/trained_model.h5'


model = load_model(MODEL_PATH)

print('Model loaded. Start serving...')


def model_predict(img_path, model):
    img = image.load_img(img_path, target_size=(64, 64)) 

    
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)

   
    preds = model.predict(img)
    
    return preds


@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
         session['data_name']  = request.form.get("nm")
         session['data_email']  = request.form.get("emal")
         session['data_phn']  = request.form.get("phn")
         session['data_age']  = int(request.form.get("age"))
         return redirect('/pnu')
    else:
        return render_template('index2.html')

@app.route('/pnu', methods = ['GET'])
def pnu():
     return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        
        f = request.files['file']

        
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)


        preds = model_predict(file_path, model)
        if preds == [[0]]:
             data_result = 'Negative'

        else:
             data_result = 'Positive'
        os.remove(file_path)

        
        data_name = session.get('data_name', 'default_value')
        data_email = session.get('data_email', 'default_value')
        data_age = session.get('data_age', 'default_value')
        data_phn = session.get('data_phn', 'default_value')
        new_patient = Patient(name = data_name, email = data_email, age = data_age, phn_number = data_phn, result = str(data_result))
        db.session.add(new_patient)
        db.session.commit()
        
        str1 = 'Pneumonia'
        str2 = 'Normal'
        if preds == 1:
            return str1
        else:
            return str2
    return None

if __name__ == '__main__':
        app.run(debug=True)

