🦴 Bone Fracture Detection System
📌 Overview
This project is a deep learning-based web application that detects bone fractures from X-ray images. It first identifies the body part (Elbow, Hand, Shoulder) and then predicts whether the bone is fractured or normal.
The system is built using Flask, TensorFlow, and ResNet50 models.

🚀 Features
1 Upload X-ray images (JPG, PNG, JPEG)
2 Automatic body part classification
3 Accurate fracture detection
4 Confidence score for predictions
5 Separate models for each body part
6 User-friendly web interface

🧠 Models Used
ResNet50 (Transfer Learning)
Body Part Classification Model
Fracture Detection Models:
1 Elbow
2 Hand
3 Shoulder
⚙️ Installation
1️⃣ Clone the Repository
git clone https://github.com/your-username/bone-fracture-detection.git
cd bone-fracture-detection
2️⃣ Install Dependencies
pip install -r requirements.txt
3️⃣ Run the Application
python app.py

🌐 Usage
1 Open browser and go to:
http://127.0.0.1:5000/
2 Upload an X-ray image
=>View prediction results instantly

📊 Results
Successfully classifies body parts: Elbow, Hand, Shoulder
Detects fractures with high accuracy using trained models
Provides confidence scores for both body part and fracture prediction
Fast and reliable predictions suitable for real-time usage

🔍 How It Works
Image is uploaded and resized to 224x224
Body part is predicted using ResNet50 model
Corresponding fracture model is selected
Final result is displayed with confidence

🧪 Technologies Used
1 Python
2 Flask
3 TensorFlow / Keras
4 NumPy
5 PIL (Image Processing)

🎯 Applications
1 Medical diagnosis assistance
2 Radiology support systems
3 AI-based healthcare tools

👨‍💻 Author
Abdul Razzak
Department of Computer Science and Engineering

📜 License
This project is for educational purposes.
