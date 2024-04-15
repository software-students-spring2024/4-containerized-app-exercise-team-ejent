"""
Pymongo: Connecting to MongoDB via Python
Flask: Python web framework
Werkzeug: WSGI utility library for Python
Base64: Encode and decode images
"""
import base64
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
#from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config["SECRET_KEY"] = "you-will-never-guess"
app.config["MONGO_CONN"] = MongoClient("mongodb://localhost:27017/")

client = app.config["MONGO_CONN"]
db = client["emotion_detection"]
temp = db["temp_store"]
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


def allowed_file(filename):
    """Check if the file extension is allowed"""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    """Render the index.html template"""
    return render_template("index.html")

count = 0
@app.route("/upload", methods=["POST"])
def upload_file():
    """Upload image file and send it to the ML model for processing"""
    global count
    if "photo" in request.files:
        photo = request.files["photo"]
        name = request.form.get("name")
        if not name:
            name = f"image_{count}"
            count += 1
        if photo.filename == "":
            return jsonify({"message": "No file selected"})
        if photo: #and allowed_file(photo.filename):
            image_data = photo.read()
            encoded = base64.b64encode(image_data).decode('utf-8')
            ins = {
                "name": name,
                "emotion": "",
                "is_processed": False,
                "photo": encoded,
            }
            temp.insert_one(ins)
            return jsonify({"message": "Image uploaded and processing started."})
        else:
            return jsonify({"message": "Invalid file type"})
    return jsonify({"message": "No file Uploaded"})

@app.route("/result")
def result():
    """Retrieve the processed document and render the result.html template"""
    retrieved = temp.find_one_and_delete({})
    if retrieved is None:
        return "No results found", 404
    name, emotion_message = retrieved["name"], retrieved["emotion"]
    emotion_message["Image"] = name
    return render_template('result.html', message=emotion_message)
if __name__ == "__main__":
    app.run(debug=True)