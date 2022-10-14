import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask import flash
from flask import send_from_directory
from keras.models import Sequential,load_model
import keras,sys
import numpy as np
from PIL import Image

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

classes = ["monkey","boar","crow"]
num_classes = len(classes)
image_size = 50

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #predict upload image
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            model = load_model("./cnn_aug.hdf5")

            image = Image.open(filepath)
            image = image.convert("RGB")
            image = image.resize((image_size,image_size))
            data = np.asarray(image)
            X = []
            X.append(data)
            X = np.array(X)

            result = model.predict([X])[0]
            predicted  = result.argmax()
            percentage = int(result[predicted]*100)

            return "ラベル： " + classes[predicted] + ", 確率："+ str(percentage) + " %"

            #return redirect(url_for('uploaded_file', name=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/uploads/<name>')
def uploaded_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)
