import PyPDF2

def read_pdf(file_path):
    """Extrait le texte brut d'un fichier PDF."""
    text = ""
    try:
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                content = page.extract_text()
                if content:
                    text += content + "\n"
        return text
    except Exception as e:
        print(f"Erreur lors de la lecture du PDF {file_path}: {e}")
        return None