"""Run this once to extract math questions from PDFs into data/maths/extracted/"""
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mathtricks.settings')
import django
django.setup()

from trainer.pdf_extractor import extract_and_cache, load_cached_only, EXTRACTED_DIR, PDF_META

EXTRACTED_DIR.mkdir(parents=True, exist_ok=True)
cached = load_cached_only()
print(f'Currently cached: {len(cached)} questions')

for pdf_name, meta in PDF_META.items():
    if meta is None:
        print(f'Skipping {pdf_name} (duplicate)')
        continue
    print(f'\nExtracting: {pdf_name}')
    try:
        questions = extract_and_cache(pdf_name)
        print(f'  -> {len(questions)} questions extracted')
        for q in questions[:2]:
            print(f'  - {q["question"][:70]}')
    except Exception as e:
        print(f'  ERROR: {e}')

print('\nDone! Total cached:', len(load_cached_only()))
