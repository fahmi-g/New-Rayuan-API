import os
import io
from keras.models import load_model
from flask import Flask, request
from keras.preprocessing.image import image_utils
import numpy as np
import json
import PIL.Image as Image
import time
import base64

app = Flask(__name__)
model = load_model('model_final.h5')
labels = ['Excellent', 'Great', 'Okay', 'Poor', 'Uncertain']

@app.route('/', methods=['POST'])
def rating():
    resImage=request.stream.read()
    decodedImage=base64.b64decode(resImage)
    imageFile=Image.open(io.BytesIO(decodedImage))

    imagePath='./images/' + time.strftime("%Y%m%d-%H%M%S") + '.jpg'
    imageFile.save(imagePath)

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