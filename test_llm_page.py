import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mathtricks.settings")
import django
django.setup()

from trainer.llm_service import get_llm_helper
import fitz, pytesseract
from PIL import Image
import io

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

doc = fitz.open(r"data\maths\olympiad\MathsOlympiad4G1.pdf")
page = doc[1]
pix = page.get_pixmap(matrix=fitz.Matrix(2.5,2.5))
img = Image.open(io.BytesIO(pix.tobytes("png")))
ocr_text = pytesseract.image_to_string(img, config="--psm 6").strip()
print("OCR snippet:", ocr_text[:300])
print()

llm = get_llm_helper()
prompt = f"""Extract math questions from this OCR text as a JSON array.
Each item: {{"q_num":1,"question":"...","type":"mcq"or"open","options":null,"answer":null,"topic":"..."}}
OCR: {ocr_text[:1000]}
Output ONLY valid JSON array:"""

raw = llm._call_llm(prompt, max_tokens=800)
print("LLM response (first 500 chars):")
print(raw[:500])
