from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
from PIL import Image
import numpy as np
from tensorflow.keras.models import load_model

app = Flask(__name__)

# Define base directory and paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'model', 'mobilenet_rcmtl_pneumonia.keras')
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load the model
model = load_model(MODEL_PATH)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def predict_image(image_path):
    img = Image.open(image_path).convert('RGB')
    img = img.resize((150, 150))  # Resize to match model input
    img_array = np.array(img) / 255.0
    img_array = img_array.reshape(1, 150, 150, 3)
    prediction = model.predict(img_array)
    return "Pneumonia" if prediction[0][0] > 0.5 else "Normal"

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/preview', methods=['GET', 'POST'])
def preview():
    if request.method == 'POST':
        if 'image' not in request.files:
            return render_template('preview.html', image_file=None)

        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            return render_template('preview.html', image_file=filename)
    return render_template('preview.html', image_file=None)


@app.route('/result')
def result():
    return render_template('result.html', result=None, image_file=None)

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return render_template('result.html', result='No image uploaded', image_file=None)

    file = request.files['image']
    if file.filename == '':
        return render_template('result.html', result='No selected file', image_file=None)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        result = predict_image(filepath)
        return render_template('result.html', result=result, image_file=filename)

    return render_template('result.html', result='Invalid file type', image_file=None)

if __name__ == '__main__':
    app.run(debug=True)
