import os
from keras.models import load_model
from flask import Flask, request, render_template
from keras.preprocessing.image import image_utils
import numpy as np
import json

app = Flask(__name__)
model = load_model('model_experiment.h5')
labels = ['Excellent', 'Great', 'Okay', 'Poor', 'Uncertain']

@app.route('/', methods=['GET'])
def rayuan():
    return render_template('interface.html')

@app.route('/', methods=['POST'])
def rating():
    resImage=request.files['imagefile']

    if resImage.filename == '':
        return render_template('test.html')

    imagePath='./images/'+resImage.filename
    resImage.save(imagePath)

    image = preprocess_image(imagePath)

    prediction=model.predict(image, batch_size=10)
    predLabel=json.dumps([{'label':labels[np.argmax(prediction)], 'certainty':str(np.max(prediction))}])

    os.remove(imagePath)

    return predLabel


def preprocess_image(input):
    image = image_utils.load_img(input, target_size=(224, 224))
    image = image_utils.img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image = np.vstack([image])

    return image

if __name__ == '__main__':
    app.run(port='80', host='0.0.0.0')