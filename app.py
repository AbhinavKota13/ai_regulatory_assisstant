from flask import Flask, render_template, request, send_file
import os
from PyPDF2 import PdfReader
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import uuid
import boto3

try:
    from docx import Document
    DOCX_AVAILABLE = True
except:
    DOCX_AVAILABLE = False


app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
GENERATED_FOLDER = "generated"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(GENERATED_FOLDER, exist_ok=True)


##############################################
# TEXT EXTRACTION
##############################################

def extract_text(file_path):

    if file_path.endswith(".pdf"):
        reader = PdfReader(file_path)
        text = ""

        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text()

        return text

    elif file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    elif file_path.endswith(".docx") and DOCX_AVAILABLE:
        doc = Document(file_path)
        return "\n".join([p.text for p in doc.paragraphs])

    return ""


##############################################
# PREVIEW GENERATOR
##############################################

def get_preview(text):
    """
    Returns first 5 lines for UI preview.
    """
    lines = text.splitlines()
    preview_lines = lines[:5]

    return "\n".join(preview_lines)


##############################################
# RISK INDICATOR
##############################################

def detect_risk_level(text):

    high_risk_keywords = [
        "safety concern",
        "adverse event",
        "serious adverse event",
        "serious risk",
        "death",
        "life-threatening",
        "hospitalization",
        "toxicity"
    ]

    text_lower = text.lower()

    for keyword in high_risk_keywords:
        if keyword in text_lower:
            return "HIGH"

    return "NORMAL"


##############################################
# AI RESPONSE
##############################################

def mock_regulatory_response(text):

    return f"""
        REGULATORY RESPONSE (Mock Output)

        Query Summary:
        The health authority has identified a potential discrepancy in the submitted regulatory documentation.

        Key Concern:
        The inconsistency may impact compliance and requires immediate clarification.

        Root Cause:
        Preliminary assessment suggests a documentation or data transcription error during submission preparation.

        Corrective Action:
        The organization will conduct a detailed review of the source data, correct the identified discrepancy, and submit an updated regulatory filing.

        Justification:
        Maintaining accurate and consistent regulatory records is critical to ensuring product quality and compliance.

        Conclusion:
        The issue will be resolved promptly, and additional validation checks will be implemented to prevent recurrence.
        """


client = boto3.client(
    "bedrock-runtime",
    region_name="us-east-1"
)

USE_REAL_AI = False   # keeping this FALSE for now


def generate_regulatory_response(text, query_type=None):

    # Always keep a fallback
    if not USE_REAL_AI:
        return mock_regulatory_response(text)

    try:

        # Prevent sending extremely large documents
        text = text[:12000]

        prompt = f"""
                You are a senior regulatory affairs specialist.

                Analyze the following health authority deficiency and generate a structured regulatory response including:

                • Query Summary  
                • Key Concern  
                • Root Cause  
                • Corrective Action  
                • Justification  
                • Conclusion  

                Use formal regulatory language suitable for submission to a health authority.

                Deficiency:
                {text}
                """

        response = client.converse(
            modelId="add_model_id",  # ← VERY IMPORTANT
            messages=[
                {
                    "role": "user",
                    "content": [{"text": prompt}]
                }
            ],
            inferenceConfig={
                "temperature": 0.2,
                "maxTokens": 400
            }
        )

        return response["output"]["message"]["content"][0]["text"]

    except Exception as e:
        print("Bedrock error:", e)

        # fallback during throttling / quota / wifi issues
        return mock_regulatory_response(text)



##############################################
# PDF CREATION
##############################################

def create_pdf(text):
    filename = f"{uuid.uuid4()}.pdf"
    file_path = os.path.join(GENERATED_FOLDER, filename)

    c = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter
    y = height - 40

    for line in text.split("\n"):

        if y < 40:
            c.showPage()
            y = height - 40

        c.drawString(40, y, line[:95])
        y -= 15

    c.save()

    return file_path


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

    # ✅ REQUIRED FILE CHECK
    if not file or file.filename.strip() == "":
        return render_template(
            "index.html",
            error="Please upload a regulatory query."
        )

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    extracted_text = extract_text(filepath)

    # Handle empty extraction
    if not extracted_text.strip():
        return render_template(
            "index.html",
            error="Unable to extract text. Please upload a valid regulatory document."
        )

    preview_text = get_preview(extracted_text)

    risk_level = detect_risk_level(extracted_text)

    ai_response = generate_regulatory_response(extracted_text, query_type)

    pdf_path = create_pdf(ai_response)

    return render_template(
        "result.html",
        response=ai_response,
        pdf_file=os.path.basename(pdf_path),
        risk_level=risk_level,
        filename=file.filename,
        preview=preview_text
    )


@app.route("/download/<filename>")
def download(filename):
    path = os.path.join(GENERATED_FOLDER, filename)
    return send_file(path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
