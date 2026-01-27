from src.aag.ingestion.pdf_reader import read_pdf

def run_extraction_pipeline(pdf_path):
    # 1. Lecture
    raw_text = read_pdf(pdf_path)
    
    # 2. Nettoyage (À implémenter demain dans text_cleaner.py)
    if raw_text:
        print(f"Extraction réussie pour : {pdf_path}")
        return raw_text
    return None