from app.main import bp
from flask import render_template, flash, redirect
import os


@bp.route('/')
@bp.route('/index')
def index():
    CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
    CLASS_NAME_PATH = os.path.join(CURRENT_PATH, '../api/keras_flowers_identification/class.txt')
    arr_classes = []
    with open(CLASS_NAME_PATH, 'r', encoding='utf-8') as f:
        arr_classes = f.readlines()
    return render_template('flower/flower.html', class_names=arr_classes)
