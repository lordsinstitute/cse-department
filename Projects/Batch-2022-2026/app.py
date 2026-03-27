from flask import Flask, render_template, request
import os
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

model = load_model("models/BC_Mobilenet.h5")

class_names = [
"Benign",
"Malignant_Pre-B",
"Malignant_Pro-B",
"Malignant_early Pre-B"
]

# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("home.html")

# ---------------- PERFORMANCE PAGES ----------------
@app.route("/cnn")
def cnn():
    return render_template("cnn.html")

@app.route("/mobilenet")
def mobilenet():
    return render_template("mnet.html")

@app.route("/resnet")
def resnet():
    return render_template("resnet.html")

# ---------------- PREDICTION ----------------
@app.route("/predict", methods=["GET","POST"])
def predict():

    prediction = None
    confidence = None
    img_path = None

    if request.method == "POST":

        file = request.files["image"]
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)

        img = image.load_img(filepath, target_size=(244, 244))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)

        img_array = preprocess_input(img_array)

        preds = model.predict(img_array)

        idx = np.argmax(preds)
        prediction = class_names[idx]
        confidence = round(float(np.max(preds))*100,2)

        img_path = filepath

    return render_template(
        "predict.html",
        prediction=prediction,
        confidence=confidence,
        img_path=img_path
    )

if __name__ == "__main__":
    app.run(debug=True)