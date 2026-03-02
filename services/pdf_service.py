import PyPDF2

def extract_pdf_text(path):
    text = ""

    try:
        with open(path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
        return text[:6000]
    except:
        return "PDF content unavailable."
