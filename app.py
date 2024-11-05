from flask import Flask, request, jsonify, render_template
from main import Pegasus_samsum
from werkzeug.utils import secure_filename
import os
import PyPDF2
import docx

app = Flask(__name__)

# Initialize the Pegasus_samsum
model_dir = "C:/Users/Umesh S/Desktop/TS-react/SummarEase/backend/model/pegasus-samsum-model"
token_dir = "C:/Users/Umesh S/Desktop/TS-react/SummarEase/backend/model/tokenizer"
summarizer = Pegasus_samsum(model_dir, token_dir)

def extract_text_from_pdf(file):
    reader = PyPDF2.PdfFileReader(file)
    text = ''
    for page_num in range(reader.numPages):
        page = reader.getPage(page_num)
        text += page.extract_text()
    return text

def extract_text_from_docx(file):
    doc = docx.Document(file)
    text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
    return text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    text = request.form.get('text', '')
    file = request.files.get('file')
    if file:
        filename = secure_filename(file.filename)
        file_ext = os.path.splitext(filename)[1].lower()

        if file_ext == '.txt':
            text = file.read().decode('utf8')
        elif file_ext == '.pdf':
            text = extract_text_from_pdf(file)
        elif file_ext == '.docx':
            file.save(os.path.join("/tmp", filename))  # Save the file temporarily
            text = extract_text_from_docx(os.path.join("/tmp", filename))
            os.remove(os.path.join("/tmp", filename))  # Clean up the file
        else:
            return jsonify({'error': 'Unsupported file type'}), 400

    if len(text.split()) > 300:
        return jsonify({'error': 'More than 300 words is not supported now.'}), 400
    
    summary = summarizer.summarize(text)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'summary': summary})
    
    return render_template('index.html', summary=summary, text=text)

if __name__ == '__main__':
    app.run(debug=True)
