from flask import Flask, render_template, request, send_file
import os

# Import service modules
from services.file_service import extract_text, get_preview
from services.risk_service import detect_risk
from services.ai_service import generate_response
from services.pdf_service import create_pdf
from services.insights_service import generate_insights

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
GENERATED_FOLDER = "generated"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(GENERATED_FOLDER, exist_ok=True)


##############################################
# ROUTES
##############################################

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():

    file = request.files.get("file")
    query_type = request.form.get("query_type")

    # Validate uploaded file
    if not file or file.filename.strip() == "":
        return render_template(
            "index.html",
            error="Please upload a regulatory query."
        )

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # Extract document text
    extracted_text = extract_text(filepath)

    if not extracted_text.strip():
        return render_template(
            "index.html",
            error="Unable to extract text. Please upload a valid regulatory document."
        )

    # Generate preview
    preview_text = get_preview(extracted_text)

    # Detect risk
    risk = detect_risk(extracted_text)

    # Generate insights based on risk level
    insights = generate_insights(risk)

    # Generate AI response
    ai_response = generate_response(
        extracted_text,
        risk,
        query_type
    )

    # Generate downloadable PDF
    pdf_path = create_pdf(ai_response)

    return render_template(
        "result.html",
        response=ai_response,
        pdf_file=os.path.basename(pdf_path),
        risk_level=risk["level"],
        risk_keywords=risk["keywords"],
        risk_reasons=risk["reasons"],
        insights=insights,
        filename=file.filename,
        preview=preview_text
    )


@app.route("/download/<filename>")
def download(filename):

    path = os.path.join(GENERATED_FOLDER, filename)

    return send_file(path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)