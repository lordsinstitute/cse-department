from flask import Flask, render_template, request
import tensorflow as tf
import numpy as np
from PIL import Image
import os
from werkzeug.utils import secure_filename
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
from views import app_exec_check

app = Flask(__name__)

app_exec_check(app)
model = tf.keras.models.load_model('saved_models_v1/best_model.h5')

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/cnn')
def cnn():
    return render_template('performance.html', folder='cnn')

@app.route('/mnet')
def mnet():
    return render_template('performance.html', folder='mnet')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'GET':
        return render_template("predict.html")

    # ✅ Check if file exists
    if 'file' not in request.files:
        return render_template("predict.html", error="No file part")

    file = request.files['file']

    # ✅ Check empty file
    if file.filename == '':
        return render_template("predict.html", error="No selected file")

    try:
        # Save file
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # Load model
        model = load_model("saved_models_cnn/best_model.h5")

        # Preprocess
        img = image.load_img(filepath, target_size=(224, 224))
        img_array = image.img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        # Predict
        pred = model.predict(img_array)[0]
        class_names = ['fake', 'real']

        predicted_class = class_names[np.argmax(pred)]
        confidence = float(np.max(pred) * 100)

        return render_template(
            "predict.html",
            prediction=predicted_class,
            confidence=confidence,
            image_path=filepath
        )

    except Exception as e:
        return render_template("predict.html", error=str(e))

if __name__ == '__main__':
    app.run(debug=True)