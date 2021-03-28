from typing import Dict
from flask import json, jsonify
import base64
import re
from PIL import Image
from werkzeug.utils import secure_filename


def make_response(is_success=True, params=None, description=''):
    if is_success:
        response = dict()
        response['Result'] = 'Success'
        response['Description'] = description
        if params is not None and isinstance(params, dict):
            response.update(params)

        return jsonify(response)
    else:
        print(f'Result: Failed, Description: {description}')
        return jsonify({'Result': 'Failed', 'Description': description})


def is_base64(s):
    pattern = re.compile("^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{4}|[A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)$")
    if not s or len(s) < 1:
        return False
    else:
        return pattern.match(s)


def request_save_image(request, image_save_path):
    failed_description = ''
    output_filename = ''
    if request.content_type.startswith('multipart/form-data'):
        # check if the post request has the file part
        if 'file' not in request.files:
            failed_description = 'File not found!'
        image_file = request.files['file']
        image_file.stream.seek(0)
        image_file.save(image_save_path)
        output_filename = secure_filename(image_file.filename)

    elif request.content_type.startswith('application/json'):
        data = request.json
        if 'base64_image' not in data:
            failed_description = 'Base64 image not found!'
        if 'filename' not in data:
            failed_description = 'Filename not found!'
        base64_image = data['base64_image'].replace('data:image/jpeg;base64,', '')
        if not isinstance(base64_image, str):
            failed_description = 'Base64 string format is incorrect'

        try:
            imgdata = base64.b64decode(base64_image)
            with open(image_save_path, 'wb') as f:
                f.write(imgdata)
            output_filename = data['filename']
        except:
            failed_description = 'Decode image is failed'
    else:
        failed_description = 'Content type is not avaliable'

    # check filename
    # if user does not select file, browser also
    # submit an empty part without filename
    if output_filename == '' or not allowed_image_filename(output_filename):
        failed_description = 'Invalid file format!'

    # test image
    try:
        Image.open(image_save_path)
    except:
        failed_description = 'Invalid image data!'

    result = 'Success'
    if failed_description != '':
        result = 'Failed'

    return {'Result': result, 'Description': failed_description, 'FileName': output_filename}


def allowed_image_filename(filename):
    IMAGE_ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in IMAGE_ALLOWED_EXTENSIONS
