import os
from flask import Flask, flash, request, redirect, url_for, render_template, send_file
from werkzeug.utils import secure_filename
import uuid
import convert
import slides
import json

UPLOAD_FOLDER = 'uploads'
CONVERT_FOLDER = 'converted'
ALLOWED_EXTENSIONS = ('json')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def convert_file(filename):
    with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), "r") as f:
        data = json.load(f)
    stories = convert.collect_stories(data)
    slides_filename = os.path.join(CONVERT_FOLDER, f"stories-{uuid.uuid4().hex[:10]}.pptx")
    slides.create_slides(stories, slides_filename)
    return slides_filename

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            slides_filename = convert_file(filename)
            return send_file(slides_filename, as_attachment=True)
    return render_template("index.html")
