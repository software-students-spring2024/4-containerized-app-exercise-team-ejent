from flask import Flask, render_template, request, jsonify
import pymongo
import os
app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'photo' in request.files:
        photo = request.files['photo']
        # Process and store the photo
        # Send photo to ML model and get results
        results = "Results from ML model"
        return jsonify({'message': 'File uploaded successfully', 'results': results})
    return jsonify({'message': 'No file uploaded'})

if __name__ == '__main__':
    app.run(debug=True)