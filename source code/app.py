from flask import Flask, render_template, request
import os
from PIL import Image
import numpy as np

app = Flask(__name__)

# Function to load and process the uploaded image
def process_image(image_file):
    # Load the image
    img = Image.open(image_file)

    # Preprocess the image (e.g., resize, normalize)

    # Perform object detection using your model
    # detection_results = your_object_detection_function(img)

    # Example placeholder:
    detection_results = {'class': ['person', 'car'], 'confidence': [0.95, 0.85]}

    return detection_results

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # Get the uploaded image file
        file = request.files['file']

        if file:
            # Save the file
            file_path = os.path.join('uploads', file.filename)
            file.save(file_path)

            # Perform object detection
            detection_results = process_image(file_path)

            # Delete the uploaded file
            os.remove(file_path)

            # Pass the detection results to the template
            return render_template('index.html', detection_results=detection_results)

if __name__ == '__main__':
    app.run(debug=True)