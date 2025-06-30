import pdfplumber

def extract_text_from_pdf(file_path):
    full_text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"
    return full_text

if __name__ == "__main__":
    file_path = "sample_bank_statement.pdf"
    text = extract_text_from_pdf(file_path)
    print(text[:1000])
