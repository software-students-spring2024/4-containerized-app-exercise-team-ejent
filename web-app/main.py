"""Main module for the web application"""
import base64
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)
app.config["SECRET_KEY"] = "you-will-never-guess"
app.config["MONGO_CONN"] = MongoClient("mongodb://localhost:27017/")

client = app.config["MONGO_CONN"]
db = client["emotion_detection"]
temp = db["temp_store"]
results_db = db["results_store"]


@app.route("/")
def index():
    """Render the index.html template"""
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file(): # pylint: disable=redefined-outer-name
    """Upload image file and send it to the ML model for processing"""
    name = request.form.get("name")
    if not name:
        return jsonify({"message": "No name provided"})
    if "photo" in request.files:
        photo = request.files["photo"]
        if photo.filename == "":
            return jsonify({"message": "No file selected"})
        if photo:
            image_data = photo.read()
            encoded = base64.b64encode(image_data).decode("utf-8")
            ins = {
                "name": name,
                "emotion": "",
                "is_processed": False,
                "photo": encoded,
            }
            temp.insert_one(ins)
            while temp.find_one({"is_processed": True}) is None:
                pass
            response = temp.find_one_and_delete({})
            temp.find_one_and_delete({"name": response["name"]})
            result = {"name": response["name"], "emotion": response["emotion"]}
            results_db.insert_one(result)

            return render_template(
                "result.html", message=response["emotion"], name=response["name"]
            )
    else:
        return jsonify({"message": "No photo provided"})


@app.after_request
def add_header(response):
    "add header"
    response.headers["Cache-Control"] = "no-store"
    return response


@app.route("/result")
def result():
    """Retrieve the processed document and render the result.html template"""
    results = list(results_db.find({}, {"_id": 0, "name": 1, "emotion": 1}))
    if not results:
        return jsonify({"message": "No processed document found"}), 404
    return render_template("result.html", results=results)


if __name__ == "__main__":
    app.run(debug=True)
