from flask import Flask, request, send_file, render_template
import fitz  # PyMuPDF
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/anonimizar', methods=['POST'])
def anonimizar_pdf():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']
    if file.filename == '':
        return "No selected file"

    words_to_anonymize = request.form.get('words').split(',')

    if file:
        input_path = os.path.join(UPLOAD_FOLDER, file.filename)
        output_path = os.path.join(OUTPUT_FOLDER, f"anonimizado_{file.filename}")
        file.save(input_path)

        # Anonimizar el PDF
        pdf_document = fitz.open(input_path)
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            for word in words_to_anonymize:
                text_instances = page.search_for(word.strip())
                for inst in text_instances:
                    page.add_redact_annot(inst, fill=(0, 0, 0))
                    page.apply_redactions()

        pdf_document.save(output_path)
        pdf_document.close()

        return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
