from flask import Flask, render_template, request, redirect, url_for, session
import fitz  # PyMuPDF
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'change_me_to_very_secret'

current_year = datetime.now().year

@app.route('/',methods=['GET', 'POST'])
def home():

    check_theme()
    return render_template("index.html", current_year=current_year)

@app.route('/name_extractor',methods=['GET', 'POST'])
def name_extractor():
    check_theme()
    return render_template('name_extractor.html', current_year=current_year)

@app.route('/about',methods=['GET', 'POST'])
def about():
    check_theme()
    return render_template('about.html', current_year=current_year)

@app.route('/contact',methods=['GET', 'POST'])
def contact():
    check_theme()
    return render_template('contact.html', current_year=current_year)


@app.route('/annotation_extractor',methods=['GET', 'POST'])
def annotation_extractor():
    check_theme()
    return render_template('annotation_extractor.html', current_year=current_year)

@app.route('/process_pdfs', methods=['GET', 'POST'])
def process_pdfs():

    check_theme()
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

def check_theme():
    if 'theme' not in session:
        session['theme'] = 'light'
    if request.method == 'POST':
        session['theme'] = 'dark' if session['theme'] == 'light' else 'light'
        return redirect(url_for('home'))
    

if __name__ == '__main__':
    app.run(debug=True)