import os
from flask import Flask, flash, request, redirect, url_for, render_template, send_file, send_from_directory
from werkzeug.utils import secure_filename
import uuid
import convert
import slides
import json

UPLOAD_FOLDER = 'uploads'
CONVERT_FOLDER = 'converted'
ALLOWED_EXTENSIONS = ('json',)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def convert_file(filename):
    stories, invalid = convert.collect_stories(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    slides_filename = f"stories-{uuid.uuid4().hex[:10]}.pptx"
    slides.create_slides(stories, os.path.join(CONVERT_FOLDER, slides_filename))
    return slides_filename, invalid


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
            slides_filename, invalid = convert_file(filename)
            invalid = [f"\"{(x[:100] + '...') if len(x) > 100 else x}\"" for x in invalid]
            return render_template("index.html", invalid_cards=invalid, download=url_for("converted_file", filename=slides_filename))
    print("Render")
    return render_template("index.html")


@app.route("/converted/<filename>")
def converted_file(filename):
    return send_from_directory(CONVERT_FOLDER, filename, as_attachment=True)
