from flask import Flask, render_template, request, send_file
from google import genai
from dotenv import load_dotenv
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
import os
import textwrap

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Get Gemini API key
GEMINI_API_KEY = os.getenv("API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set in the .env file")

# Create Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)

# Current Gemini model
MODEL_NAME = "gemini-3.7-flash"

# Create output folder
OUTPUT_FOLDER = "outputs"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():

    topic = request.form.get("topic", "").strip()
    level = request.form.get("level", "Beginner")
    length = request.form.get("length", "Medium")

    if not topic:
        return render_template(
            "index.html",
            error="Please enter a topic."
        )

    # Define explanation length
    length_instruction = {
        "Short": "Explain in approximately 150 words.",
        "Medium": "Explain in approximately 300 words.",
        "Long": "Explain in approximately 500 words."
    }

    prompt = f"""
You are an expert educational AI tutor.

Explain the following topic clearly and accurately:

Topic: {topic}

Audience Level: {level}

{length_instruction.get(length, length_instruction["Medium"])}

Follow these requirements:

1. Start with a simple definition.
2. Explain the concept in easy-to-understand language.
3. Give important points.
4. Give a practical example.
5. Use headings and bullet points where appropriate.
6. If applicable, explain advantages and disadvantages.
7. End with a short summary.
8. Avoid unnecessary technical jargon.
9. Make the explanation useful for a student.
"""

    try:

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        explanation = response.text

        return render_template(
            "index.html",
            topic=topic,
            level=level,
            length=length,
            explanation=explanation
        )

    except Exception as e:

        return render_template(
            "index.html",
            error=f"Gemini API Error: {str(e)}"
        )


@app.route("/download_txt", methods=["POST"])
def download_txt():

    explanation = request.form.get("explanation", "")
    topic = request.form.get("topic", "topic")

    filename = os.path.join(
        OUTPUT_FOLDER,
        "topic_explanation.txt"
    )

    with open(filename, "w", encoding="utf-8") as file:
        file.write(f"TOPIC: {topic}\n")
        file.write("=" * 60 + "\n\n")
        file.write(explanation)

    return send_file(
        filename,
        as_attachment=True,
        download_name=f"{topic}_explanation.txt"
    )


@app.route("/download_pdf", methods=["POST"])
def download_pdf():

    explanation = request.form.get("explanation", "")
    topic = request.form.get("topic", "topic")

    filename = os.path.join(
        OUTPUT_FOLDER,
        "topic_explanation.pdf"
    )

    pdf = canvas.Canvas(filename, pagesize=A4)

    width, height = A4

    left_margin = 50
    right_margin = 50
    top_margin = height - 50

    y = top_margin

    # Title
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(
        left_margin,
        y,
        "AI Topic Explainer"
    )

    y -= 35

    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(
        left_margin,
        y,
        f"Topic: {topic}"
    )

    y -= 30

    pdf.setFont("Helvetica", 10)

    # Split text into lines
    lines = []

    for paragraph in explanation.split("\n"):

        if paragraph.strip():

            wrapped = simpleSplit(
                paragraph,
                "Helvetica",
                10,
                width - left_margin - right_margin
            )

            lines.extend(wrapped)

        else:
            lines.append("")

    # Write text
    for line in lines:

        if y < 50:

            pdf.showPage()
            pdf.setFont("Helvetica", 10)
            y = top_margin

        pdf.drawString(
            left_margin,
            y,
            line
        )

        y -= 15

    pdf.save()

    return send_file(
        filename,
        as_attachment=True,
        download_name=f"{topic}_explanation.pdf"
    )


if __name__ == "__main__":
    app.run(debug=True)
