# Language & Format Converter (Flask)

A working starter project to upload a file, translate its contents to a selected language, and convert the output into TXT/DOCX/PDF with a clean, modern UI.

## Features
- Upload: TXT, DOCX, PDF
- Auto-detect language (best-effort) and translate to a target language
- Convert to: TXT, DOCX, or PDF
- Download link after processing
- Tailwind UI + drag-and-drop uploader

## Quick Start

```bash
# 1) Create and activate a virtual environment (recommended)
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# 2) Install dependencies
pip install -r requirements.txt

# 3) Run the app
python app/main.py

# App runs on http://127.0.0.1:5000
```

## Notes
- Internet connection is required for online translation providers.
- If translation provider fails, the app falls back to a simple "pass-through" (no translation) so the pipeline still produces a file.
- PDF generation is simple text-based (via reportlab) for robustness.
