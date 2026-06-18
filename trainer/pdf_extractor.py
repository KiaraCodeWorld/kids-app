"""
PDF Math Question Extractor
Renders PDF pages → OCR with pytesseract → LLM parses into structured JSON.
Caches extracted questions as JSON in data/maths/extracted/.
"""
import os
import json
import re
import logging
import hashlib
from pathlib import Path

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent
MATHS_DIR = BASE_DIR / 'data' / 'maths'
EXTRACTED_DIR = BASE_DIR / 'data' / 'maths' / 'extracted'

try:
    import fitz  # PyMuPDF
    _FITZ_OK = True
except ImportError:
    _FITZ_OK = False

try:
    import pytesseract
    from PIL import Image
    import io
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    _OCR_OK = True
except ImportError:
    _OCR_OK = False


PDF_META = {
    'MathsOlympiad4G1.pdf': {
        'grade': 4, 'age_min': 9, 'age_max': 11,
        'source': 'Math Olympiad Grade 4', 'difficulty': 'olympiad',
        'type_hint': 'open',
    },
    '4th-math.pdf': {
        'grade': 4, 'age_min': 9, 'age_max': 11,
        'source': '4th Grade Math Practice', 'difficulty': 'standard',
        'type_hint': 'mixed',
    },
    '5.+Jupitor,+Grade+4.pdf': {
        'grade': 4, 'age_min': 9, 'age_max': 11,
        'source': 'Jupiter Grade 4', 'difficulty': 'enrichment',
        'type_hint': 'mixed',
    },
    'december-grade-3-4-questions-and-solutions-olympiadusa-org.pdf': {
        'grade': 4, 'age_min': 8, 'age_max': 11,
        'source': 'Olympiad USA Gr 3-4', 'difficulty': 'olympiad',
        'type_hint': 'mcq',
    },
    'MathsOlympiad4G1 (1).pdf': None,  # duplicate — skip
}


def _ocr_page(page, scale=2.5) -> str:
    if not (_FITZ_OK and _OCR_OK):
        return ''
    pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale))
    img = Image.open(io.BytesIO(pix.tobytes('png')))
    text = pytesseract.image_to_string(img, config='--psm 6')
    return text.strip()


def _llm_parse_questions(ocr_text: str, meta: dict, page_num: int) -> list[dict]:
    """Send OCR text to LLM and get structured question JSON back."""
    from .llm_service import get_llm_helper
    llm = get_llm_helper()
    if not llm:
        return []

    grade = meta.get('grade', 4)
    source = meta.get('source', 'Math')
    type_hint = meta.get('type_hint', 'mixed')

    type_desc = {
        'mcq': 'multiple-choice (A/B/C/D)',
        'open': 'open-ended / fill-in-the-blank',
        'mixed': 'mixed (some multiple-choice, some open-ended)',
    }.get(type_hint, 'mixed')

    prompt = f"""You are extracting math questions from OCR text of a Grade {grade} worksheet.
The questions are {type_desc}.

OCR TEXT (page {page_num} of "{source}"):
---
{ocr_text[:3000]}
---

Extract EVERY question visible. Return a JSON array. Each item:
{{
  "q_num": <integer question number>,
  "question": "<full question text, clean>",
  "type": "mcq" or "open",
  "options": {{"A": "...", "B": "...", "C": "...", "D": "..."}} or null,
  "answer": "<correct answer or null if not shown>",
  "topic": "<topic like Place Value, Addition, Fractions, etc>"
}}

Rules:
- question text must be complete and self-contained
- For mcq: extract all options even if labeled a/b/c or 1/2/3 or A/B/C/D
- For open/fill-in: type="open", options=null
- If answer key present, fill answer. Otherwise answer=null
- Ignore headers, instructions, page numbers, watermarks
- Output ONLY the JSON array, no prose

JSON:"""

    try:
        raw = llm._call_llm(prompt, max_tokens=1200)
        if not raw:
            logger.warning(f'LLM returned empty response for page {page_num}')
            return []

        # Strip markdown code fences
        raw = re.sub(r'```(?:json)?\s*', '', raw).strip()

        # Try to find JSON array
        match = re.search(r'\[.*?\]', raw, re.DOTALL)
        if not match:
            # Try wrapping single object in array
            obj_match = re.search(r'\{.*?\}', raw, re.DOTALL)
            if obj_match:
                try:
                    obj = json.loads(obj_match.group())
                    return [obj] if isinstance(obj, dict) else []
                except Exception:
                    pass
            logger.warning(f'LLM returned no JSON array for page {page_num}: {raw[:120]}')
            return []

        questions = json.loads(match.group())
        return questions if isinstance(questions, list) else []
    except Exception as e:
        logger.warning(f'LLM parse failed page {page_num}: {e}')
        return []


def extract_pdf(pdf_path: Path, meta: dict, max_pages=20) -> list[dict]:
    """Extract all questions from a PDF file."""
    if not _FITZ_OK:
        logger.error('PyMuPDF not available')
        return []

    doc = fitz.open(str(pdf_path))
    all_questions = []
    q_counter = 1

    for page_num in range(min(len(doc), max_pages)):
        page = doc[page_num]
        ocr_text = _ocr_page(page)
        if len(ocr_text.strip()) < 30:
            continue  # blank or non-content page

        parsed = _llm_parse_questions(ocr_text, meta, page_num + 1)

        for q in parsed:
            if not q.get('question') or len(q.get('question', '')) < 8:
                continue
            q_id = f"{meta.get('source', 'math').lower().replace(' ', '_')}_p{page_num+1}_q{q.get('q_num', q_counter)}"
            q_id = re.sub(r'[^a-z0-9_]', '', q_id)[:60]
            all_questions.append({
                'id': q_id,
                'question': q.get('question', ''),
                'type': q.get('type', 'open'),
                'options': q.get('options'),
                'answer': q.get('answer'),
                'topic': q.get('topic', 'General Math'),
                'grade': meta.get('grade', 4),
                'age_min': meta.get('age_min', 8),
                'age_max': meta.get('age_max', 12),
                'difficulty': meta.get('difficulty', 'standard'),
                'source': meta.get('source', 'Math'),
                'page': page_num + 1,
            })
            q_counter += 1

    doc.close()
    return all_questions


def get_cache_path(pdf_name: str) -> Path:
    slug = re.sub(r'[^a-z0-9]', '_', pdf_name.lower())[:40]
    return EXTRACTED_DIR / f'{slug}.json'


def extract_and_cache(pdf_name: str, force=False) -> list[dict]:
    """Extract questions from PDF, using cache if available."""
    meta = PDF_META.get(pdf_name)
    if meta is None:
        return []  # skip duplicates / unknown

    EXTRACTED_DIR.mkdir(parents=True, exist_ok=True)
    cache_path = get_cache_path(pdf_name)

    if cache_path.exists() and not force:
        try:
            with open(cache_path, encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass

    pdf_path = MATHS_DIR / 'olympiad' / pdf_name
    if not pdf_path.exists():
        # search all subdirs
        for p in MATHS_DIR.rglob(pdf_name):
            pdf_path = p
            break

    if not pdf_path.exists():
        logger.warning(f'PDF not found: {pdf_name}')
        return []

    logger.info(f'Extracting questions from {pdf_name}...')
    questions = extract_pdf(pdf_path, meta)
    logger.info(f'Extracted {len(questions)} questions from {pdf_name}')

    with open(cache_path, 'w', encoding='utf-8') as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)

    return questions


def load_all_questions() -> list[dict]:
    """Load all extracted questions from cache. Extract if missing."""
    all_q = []
    for pdf_name, meta in PDF_META.items():
        if meta is None:
            continue
        questions = extract_and_cache(pdf_name)
        all_q.extend(questions)

    # Deduplicate by question text
    seen = set()
    unique = []
    for q in all_q:
        key = q['question'][:80].lower().strip()
        if key not in seen:
            seen.add(key)
            unique.append(q)

    return unique


def load_cached_only() -> list[dict]:
    """Load only already-cached questions (no extraction)."""
    all_q = []
    if not EXTRACTED_DIR.exists():
        return []
    for cache_file in EXTRACTED_DIR.glob('*.json'):
        try:
            with open(cache_file, encoding='utf-8') as f:
                all_q.extend(json.load(f))
        except Exception:
            continue
    # Deduplicate
    seen = set()
    unique = []
    for q in all_q:
        key = q['question'][:80].lower().strip()
        if key not in seen:
            seen.add(key)
            unique.append(q)
    return unique
