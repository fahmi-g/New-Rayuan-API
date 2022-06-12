import os
import io
from keras.models import load_model
from flask import Flask, request, jsonify, session, app
from datetime import timedelta
from keras.preprocessing.image import image_utils
import numpy as np
import PIL.Image as Image
import time
import base64

api = Flask(__name__)
model = load_model('latest_model.h5')
labels = ['Excellent', 'Great', 'Okay', 'Uncertain', 'Poor']

@api.route('/', methods=['POST'])
def rating():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=10)

    resImage=request.stream.read()
    decodedImage=base64.b64decode(resImage)
    imageFile=Image.open(io.BytesIO(decodedImage))

    imagePath='./images/' + time.strftime("%Y%m%d-%H%M%S") + '.png'
    imageFile.save(imagePath)

    image = preprocess_image(imagePath)

    prediction=model.predict(image, batch_size=10)
    predLabel=jsonify({'label':labels[np.argmax(prediction)], 'certainty':str(np.max(prediction))})

    os.remove(imagePath)

    return predLabel


def preprocess_image(input):
    image = image_utils.load_img(input, target_size=(224, 224))
    image = image_utils.img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image = np.vstack([image])

    return image

if __name__ == '__main__':
    api.run(port='80', host='0.0.0.0')