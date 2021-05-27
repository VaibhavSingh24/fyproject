from threading import main_thread
from flask import Flask, render_template,flash, request, redirect, url_for
import os
import pytesseract as pt
pt.pytesseract.tesseract_cmd = r'Tesseract-OCR//tesseract.exe'

# /app/.apt/usr/bin/tesseract
# Tesseract-OCR//tesseract.exe

UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.secret_key = "a7570aa1"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# This returns template
@app.route('/')
def home():
    return render_template('index.html')


# this handles image upload
@app.route('/', methods = ['POST'])
def imgupload():
    if 'file' not in request.files:
        flash('NO FILE PART')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for upload')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        file.save(os.path.join(app.config['UPLOAD_FOLDER'],file.filename))
        flash('upload success')
        print(file.filename)
        prtext = pt.image_to_string(os.path.join(app.config['UPLOAD_FOLDER'],file.filename))
        
        try:
            return render_template('index.html',filename = file.filename, pred_text = prtext )
        except:
            return render_template('index.html',filename = file.filename, pred_text = "internal error" )

    else:
        flash("Upload image only")
        return redirect(request.url)


# # this displays the file
# @app.route("/<filename>")
# def display_image(filename):
#     return redirect(url_for('static', filename='uploads/' + filename), code=301)

@app.route("/about")
def predict_text():
    return render_template("about.html")

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000)   