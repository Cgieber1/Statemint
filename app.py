from flask import Flask, render_template, request, send_file
import os
from extract_bank_data import extract_text_from_pdf
from gpt_cleaner import clean_bank_text_with_gpt, save_to_csv

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        pdf = request.files["bank_pdf"]
        if pdf.filename.endswith(".pdf"):
            file_path = os.path.join(UPLOAD_FOLDER, pdf.filename)
            pdf.save(file_path)

            raw_text = extract_text_from_pdf(file_path)
            cleaned_text = clean_bank_text_with_gpt(raw_text)
            csv_path = os.path.join(UPLOAD_FOLDER, "cleaned_statement.csv")
            save_to_csv(cleaned_text, filename=csv_path)

            return send_file(csv_path, as_attachment=True)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

