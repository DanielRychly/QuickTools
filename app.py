from flask import Flask, render_template, request, redirect, url_for, session
import fitz  # PyMuPDF
from datetime import datetime
import io

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

@app.route('/output_highlights',methods=['GET', 'POST'])
def output_highlights():

    if 'pdf_file' not in request.files:
        return 'No file part'
    
    file = request.files['pdf_file']
    
    if file and file.filename.endswith('.pdf'):
        # Read the file content into a stream
        file_stream = io.BytesIO(file.read())

        with fitz.open(stream=file_stream, filetype="pdf") as doc:

            # taking page for further processing
            all_highlights = ""

            for page in doc:

                # list to store the co-ordinates of all highlights
                highlights = []

                # loop till we have highlight annotation in the page
                annot = page.first_annot
                while annot:
                    if annot.type[0] == 8:
                        all_coordinates = annot.vertices
                        if len(all_coordinates) == 4:
                            highlight_coord = fitz.Quad(all_coordinates).rect
                            highlights.append(highlight_coord)
                        else:
                            all_coordinates = [all_coordinates[x:x+4] for x in range(0, len(all_coordinates), 4)]
                            for i in range(0,len(all_coordinates)):
                                coord = fitz.Quad(all_coordinates[i]).rect
                                highlights.append(coord)
                    annot = annot.next

                all_words = page.get_text_words()

                # List to store all the highlighted texts
                highlight_text = []

                for h in highlights:
                
                    sentence = [w[4] for w in all_words if fitz.Rect(w[0:4]).intersects(h)]
                    highlight_text.append(" ".join(sentence))

                row = " ".join(highlight_text)

                all_highlights = all_highlights + row + '\n'

        return render_template('output_highlights.html', current_year=current_year, all_highlights=all_highlights)


@app.route('/process_pdfs', methods=['GET', 'POST'])
def process_pdfs():

    check_theme()

    if 'pdf_files[]' not in request.files:
        return 'No file part'
    
    files = request.files.getlist('pdf_files[]')
    
    filenames = [file.filename for file in files if file.filename != '']
    
    # Here you can add your own logic to process the PDFs

    output_page = '<h1>Uploaded Files</h1>'
    output_page += '<form action="/submit_filenames" method="post">'
    output_page += '<table style="width:100%;">'
    
    for index, filename in enumerate(filenames, start=1):
        output_page += f'<tr><td>{index}</td><td><input type="text" value="{filename}" style="width:100%;"></td></tr>'
    
    output_page += '</table>'
    output_page += '<input type="submit" value="Submit">'
    output_page += '</form>'
   # return output_page  # TODO output table here

    """
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
    """
    return render_template('process_pdfs.html', current_year=current_year, output_page=output_page)

@app.route('/submit_filenames', methods=['GET', 'POST'])
def submit_filenames():
    return render_template('submit_filenames.html', current_year=current_year)


def check_theme():
    if 'theme' not in session:
        session['theme'] = 'light'
    if request.method == 'POST':
        session['theme'] = 'dark' if session['theme'] == 'light' else 'light'
        return redirect(url_for('home'))
    

if __name__ == '__main__':
    app.run(debug=True)