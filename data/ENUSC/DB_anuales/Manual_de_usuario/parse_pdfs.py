import os
from pypdf import PdfReader
import re

pdf_dir = r"C:\Users\Asvaldebenitom\OneDrive - Instituto Nacional de Estadisticas\Artículos\Trayectoria_delictual_Chile\data\ENUSC\DB_anuales\Manual_de_usuario"

pdfs = [f for f in os.listdir(pdf_dir) if f.endswith('.pdf')]
results = {}

keywords = ['representatividad', 'comuna', 'comunales', 'expansión', 'muestra', 'diseño muestral', 'estratificado', 'fact_hog']

for pdf_file in pdfs:
    path = os.path.join(pdf_dir, pdf_file)
    year_match = re.search(r'20\d{2}', pdf_file)
    year = year_match.group() if year_match else pdf_file
    results[year] = []
    
    try:
        reader = PdfReader(path)
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if not text: continue
            
            # Simple heuristic: look for paragraphs with numbers and our keywords together
            text_lower = text.lower()
            if any(k in text_lower for k in keywords):
                # Extract surrounding sentences around keywords
                sentences = re.split(r'(?<=[.!?])\s+', text)
                for s in sentences:
                    s_lower = s.lower()
                    if ('comuna' in s_lower or 'representatividad' in s_lower) and any(char.isdigit() for char in s):
                        if len(s) > 20 and len(s) < 300:
                            results[year].append(f"Page {i+1}: {s.strip().replace('\n', ' ')}")
    except Exception as e:
        results[year] = [f"Error reading {pdf_file}"]

import json
with open('pdf_summary.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=4)
print("PDF extraction complete.")
