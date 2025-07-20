from flask import Flask, render_template, request, send_file, redirect, url_for
import os
from werkzeug.utils import secure_filename
import PyPDF2

app = Flask(__name__)

# Use absolute path to uploads folder
basedir = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(basedir, 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Homepage
@app.route('/')
def index():
    return render_template('index.html')

# PDF Merge Route
@app.route('/merge', methods=['POST'])
def merge_pdfs():
    pdfs = request.files.getlist('pdfs')
    merger = PyPDF2.PdfMerger()

    for pdf in pdfs:
        if pdf.filename.endswith('.pdf'):
            filename = secure_filename(pdf.filename)
            path = os.path.join(UPLOAD_FOLDER, filename)
            pdf.save(path)
            merger.append(path)

    output_path = os.path.join(UPLOAD_FOLDER, 'merged.pdf')
    with open(output_path, 'wb') as f:
        merger.write(f)

    return send_file(output_path, as_attachment=True)

# PDF Split Route (POST)
@app.route('/split', methods=['POST'])
def split_pdf():
    pdf = request.files['pdf']
    start_page = int(request.form['start'])
    end_page = int(request.form['end'])

    input_path = os.path.join(UPLOAD_FOLDER, secure_filename(pdf.filename))
    pdf.save(input_path)

    reader = PyPDF2.PdfReader(input_path)
    writer = PyPDF2.PdfWriter()

    for i in range(start_page - 1, end_page):
        if i < len(reader.pages):
            writer.add_page(reader.pages[i])

    output_path = os.path.join(UPLOAD_FOLDER, 'split.pdf')
    with open(output_path, 'wb') as f:
        writer.write(f)

    return send_file(output_path, as_attachment=True)

# PDF Split Route (GET) → Redirect to home
@app.route('/split', methods=['GET'])
def split_get():
    return redirect(url_for('index'))

# Run App
if __name__ == '__main__':
    app.run(debug=True)
