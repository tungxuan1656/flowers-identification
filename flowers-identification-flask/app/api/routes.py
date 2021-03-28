from app.api import bp
import os
from flask import request
import time
from app.main.utils import make_response, request_save_image
from PIL import Image
from app.api.keras_flowers_identification.model import get_model, prediction
import numpy as np

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(CURRENT_PATH, 'keras_flowers_identification/17flowers_weights.h5')
IMAGE_UPLOAD_FOLDER = os.path.join(CURRENT_PATH, '../../logs/image_upload')
IMAGE_PATH = os.path.join(CURRENT_PATH, 'image.jpg')
CLASS_NAMES_PATH = os.path.join(CURRENT_PATH, 'keras_flowers_identification/class.txt')
FILENAME = ''

arr_names = []
with open(CLASS_NAMES_PATH, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    arr_names = list(map(lambda x: x.replace('\n', ''), lines))

if not os.path.exists(IMAGE_UPLOAD_FOLDER):
    os.mkdir(IMAGE_UPLOAD_FOLDER)

# model = predict.load_model(MODEL_PATH)
# predict.classify(model, IMAGE_PATH)

model = get_model()
model.load_weights(MODEL_PATH)


@bp.route('/flower/identification', methods=['GET', 'POST'])
def flowers_identification():
    if request.method == 'GET':
        return make_response(False, description='The get method is not available')

    receive_image = request_save_image(request, IMAGE_PATH)
    if receive_image['Result'] != 'Success':
        return make_response(False, description=receive_image['Description'])
    else:
        FILENAME = receive_image['FileName']

    start = time.time()
    predict = prediction(model, IMAGE_PATH)
    class_id = int(np.argmax(predict))
    confident = round(float(predict[class_id]), 2)
    # Prediction image
    result = {'ClassID': class_id + 1, 'ClassName': arr_names[class_id], 'Confident': confident}

    basename, ext = os.path.splitext(FILENAME)
    basename += time.strftime("_%Y%m%d_%H%M%S")
    basename += f'_classid_{class_id}'
    FILENAME = basename + ext

    im = Image.open(IMAGE_PATH)
    im_resize = im.resize((int(im.width * 256 / im.height), 256))
    im_resize.save(os.path.join(IMAGE_UPLOAD_FOLDER, FILENAME))
    print(f'Model classify in {time.time() - start} seconds. Result: {result}. File: {FILENAME}')

    return make_response(True, result, '')
