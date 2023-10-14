from flask import Flask, render_template, request
import fitz  # PyMuPDF
from datetime import datetime

app = Flask(__name__)

current_year = datetime.now().year

@app.route('/')
def home():
    
    return render_template("index.html", current_year=current_year)

@app.route('/name_extractor')
def name_extractor():
    return render_template('name_extractor.html', current_year=current_year)

@app.route('/about')
def about():
    return render_template('about.html', current_year=current_year)

@app.route('/annotation_extractor')
def annotation_extractor():
    return render_template('annotation_extractor.html', current_year=current_year)

@app.route('/process_pdfs', methods=['GET', 'POST'])
def process_pdfs():

    uploaded_file = request.files['pdf_file']  # Get a single uploaded PDF file
    parsed_text = ''

    # Check if the file is a PDF
    if uploaded_file and uploaded_file.filename.endswith('.pdf'):
        pdf_document = fitz.open(stream=uploaded_file.read(), filetype='pdf')

        # Extract text from each page and concatenate
        for page_num in range(pdf_document.page_count):
            page = pdf_document.load_page(page_num)
            parsed_text += page.get_text()
    else:
        return "Invalid file format. Please upload a PDF file."

    # Now, you can initiate your parsing logic with the parsed_text
    # For example, you can send the parsed_text to a function for further processing

    return render_template('process_pdfs.html', parsed_text=parsed_text, current_year=current_year)

if __name__ == '__main__':
    app.run(debug=True)