import numpy as np
import torch
from PIL import Image
from flask import Flask, request, send_file, jsonify

PATH = './source/mnist_model.pt'
model = torch.load(PATH)

file_formats = ['jpg', 'png']

app = Flask(__name__)

def load_image(filename):
    # load the image
    img = Image.open(filename)
    # convert to array
    img = np.array(img)
    # reshape into input format
    img = img.reshape(1, 784)
    # prepare pixel data
    img = img.astype('float32')
    img = img / 255.0
    return img

@app.route("/")
def home():
    return "Hello, World!"

@app.route('/check_num', methods=['POST'])
def check_num():
    # Check if a file was included in the POST request
    if 'file' not in request.files:
        return 'No file included in request'
    
    # Get the file from the request
    file = request.files['file']
    
    # Check if the file has a valid name
    if file.filename.split('.')[1] not in file_formats:
        return 'Invalid image format'
    
    img = load_image(file)
    img = torch.from_numpy(img)
    with torch.no_grad():
            logps = model(img)
    ps = torch.exp(logps)
    probab = list(ps.numpy()[0])
    pred_label = probab.index(max(probab))

    # Return a response
    return jsonify({'The number in the image is' : pred_label})
    
if __name__ == "__main__":
    # app.run(debug=False)
    app.run(debug=True, host='0.0.0.0', port=5000)
