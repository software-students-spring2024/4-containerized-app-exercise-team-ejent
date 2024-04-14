from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from werkzeug.utils import secure_filename
import os
app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'
db = MongoClient('mongodb://localhost:27017/')['webapp']
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')
    #can u edit the upload files method to insert the image, probably encoded, into the db
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'photo' in request.files:
        photo = request.files['photo']
        if photo.filename == '':
            return jsonify({'message': 'No file selected'})
        if photo and allowed_file(photo.filename):
            filename = secure_filename(photo.filename)
            # Process and store the photo
            photo_data = photo.read()
            encoded_photo = Binary(photo_data)
            db.photos.insert_one({'photo': encoded_photo})

            #Placeholder: send photo to ML model and get results
            results = "results from ml model"
            return jsonify({'message': 'File uploaded successfully', 'results': results})
        else:
            return jsonify({'message': 'Invalid file type'})
    return jsonify({'message': 'No file Uploaded'})

            

if __name__ == '__main__':
    app.run(debug=True)

