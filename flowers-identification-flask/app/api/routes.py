from app.api import bp
import os
from flask import request
import time
from app.main.utils import make_response, is_base64
from werkzeug.utils import secure_filename
from PIL import Image
from io import BytesIO
import base64


CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(CURRENT_PATH, 'keras_open_nsfw/nsfw_mobilenet2.h5')
IMAGE_UPLOAD_FOLDER = os.path.join(CURRENT_PATH, '../../logs/image_upload')
IMAGE_PATH = os.path.join(CURRENT_PATH, 'image.jpg')
IMAGE_ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
FILENAME = ''

if not os.path.exists(IMAGE_UPLOAD_FOLDER):
    os.mkdir(IMAGE_UPLOAD_FOLDER)

# model = predict.load_model(MODEL_PATH)
# predict.classify(model, IMAGE_PATH)


@bp.route('/nsfw/check', methods=['GET', 'POST'])
def classify_photo_nsfw():
    if request.method == 'GET':
        return make_response(False, description='The get method is not available')

    if request.content_type.startswith('multipart/form-data'):
        # check if the post request has the file part
        if 'file' not in request.files:
            return make_response(False, description='File not found!')
        image_file = request.files['file']
        image_file.stream.seek(0)
        image_file.save(IMAGE_PATH)
        FILENAME = secure_filename(image_file.filename)

    elif request.content_type.startswith('application/json'):
        data = request.json
        if 'base64_image' not in data:
            return make_response(False, description='Base64 image not found!')
        if 'filename' not in data:
            return make_response(False, description='Filename not found!')
        base64_image = data['base64_image'].replace('data:image/jpeg;base64,', '')
        if not isinstance(base64_image, str):
            return make_response(False, description='Base64 string format is incorrect')

        try:
            imgdata = base64.b64decode(base64_image)
            with open(IMAGE_PATH, 'wb') as f:
                f.write(imgdata)
            FILENAME = data['filename']
        except:
            return make_response(False, description='Decode image is failed')
    else:
        return make_response(False, description='Content type is not avaliable')

    # check filename
    # if user does not select file, browser also
    # submit an empty part without filename
    if FILENAME == '' or not allowed_file(FILENAME):
        return make_response(False, description='Invalid file format!')

    # test image
    try:
        Image.open(IMAGE_PATH)
    except:
        return make_response(False, description='Invalid image data!')

    # Prediction image
    result = {'Key': 'Value'}
    return make_response(True, result, '')


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in IMAGE_ALLOWED_EXTENSIONS
