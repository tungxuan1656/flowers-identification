from app.main import bp
from flask import render_template, flash, redirect


@bp.route('/')
@bp.route('/index')
def index():
    return render_template('flower/flower.html')
