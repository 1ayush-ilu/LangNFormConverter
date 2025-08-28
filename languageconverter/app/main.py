import os
from datetime import datetime
from flask import Flask, render_template, request, send_from_directory, jsonify, url_for
from werkzeug.utils import secure_filename

from utils import (
    extract_text_from_file,
    detect_language,
    translate_text,
    save_as_txt,
    save_as_docx,
    save_as_pdf,
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)

UPLOAD_FOLDER = os.path.join(ROOT_DIR, "uploads")
OUTPUT_FOLDER = os.path.join(ROOT_DIR, "outputs")
ALLOWED_EXTENSIONS = {".txt", ".docx", ".pdf"}

app = Flask(__name__, template_folder=os.path.join(BASE_DIR, "templates"), static_folder=os.path.join(BASE_DIR, "static"))
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["OUTPUT_FOLDER"] = OUTPUT_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024  # 50 MB

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def allowed_file(filename: str) -> bool:
    _, ext = os.path.splitext(filename.lower())
    return ext in ALLOWED_EXTENSIONS

@app.get("/")
def index():
    return render_template("index.html")

@app.post("/process")
def process():
    if "file" not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Unsupported file type. Use TXT, DOCX, or PDF."}), 400

    target_lang = request.form.get("target_lang", "en").strip().lower()
    output_format = request.form.get("output_format", "txt").strip().lower()

    filename = secure_filename(file.filename)
    save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(save_path)

    try:
        # Extract & translate
        text = extract_text_from_file(save_path)
        detected = detect_language(text)
        translated = translate_text(text, target_lang)

        # Save in chosen format
        if output_format == "txt":
            out_path = save_as_txt(translated, app.config["OUTPUT_FOLDER"])
        elif output_format == "docx":
            out_path = save_as_docx(translated, app.config["OUTPUT_FOLDER"])
        elif output_format == "pdf":
            out_path = save_as_pdf(translated, app.config["OUTPUT_FOLDER"])
        else:
            return jsonify({"error": "Invalid output format"}), 400

        out_name = os.path.basename(out_path)
        download_url = url_for('download_file', filename=out_name)

        return jsonify({
            "message": "Success",
            "detected_lang": detected,
            "target_lang": target_lang,
            "output_name": out_name,
            "download_url": download_url
        }), 200

    except Exception as e:
        return jsonify({"error": f"Processing failed: {e}"}), 500

@app.get("/download/<path:filename>")
def download_file(filename):
    return send_from_directory(app.config["OUTPUT_FOLDER"], filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
