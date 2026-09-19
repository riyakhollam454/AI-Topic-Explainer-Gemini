import os
import json


from pypdf import PdfReader
from dotenv import load_dotenv
from google import genai

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()

# -----------------------------
# Gemini Client
# -----------------------------
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# -----------------------------
# File paths
# -----------------------------
PDF_PATH = r"C:\Users\riyak\Downloads\Student_Data_Science_Data_Analysis_GenAI_Handbook.pdf"

OUTPUT_FILE = "knowledge_base.json"

# -----------------------------
# Chunk settings
# -----------------------------
CHUNK_SIZE = 1200
CHUNK_OVERLAP = 200


# -----------------------------
# Extract PDF text
# -----------------------------
def extract_pdf():

    reader = PdfReader(PDF_PATH)

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):

        text = page.extract_text()

        if text:

            text = text.strip()

            pages.append({
                "page": page_number,
                "text": text
            })

    return pages


# -----------------------------
# Create chunks
# -----------------------------
def create_chunks(pages):

    chunks = []

    for page_data in pages:

        page_number = page_data["page"]
        text = page_data["text"]

        start = 0

        while start < len(text):

            end = start + CHUNK_SIZE

            chunk_text = text[start:end]

            chunks.append({
                "page": page_number,
                "text": chunk_text
            })

            start += CHUNK_SIZE - CHUNK_OVERLAP

    return chunks


# -----------------------------
# Create embeddings
# -----------------------------
def create_embeddings(chunks):

    print("Creating embeddings...")

    for i, chunk in enumerate(chunks):

        print(
            f"Embedding chunk {i + 1}/{len(chunks)}"
        )

        result = client.models.embed_content(
            model="gemini-embedding-001",
            contents=chunk["text"]
        )

        embedding = result.embeddings[0].values

        chunk["embedding"] = embedding

    return chunks


# -----------------------------
# Save knowledge base
# -----------------------------
def save_knowledge_base(chunks):

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            chunks,
            file,
            ensure_ascii=False
        )

    print("\nKnowledge base created successfully.")

    print(
        f"Saved to: {OUTPUT_FILE}"
    )


# -----------------------------
# Main
# -----------------------------
def main():

    print("Reading PDF...")

    pages = extract_pdf()

    print(
        f"Extracted {len(pages)} pages."
    )

    print("\nCreating chunks...")

    chunks = create_chunks(pages)

    print(
        f"Created {len(chunks)} chunks."
    )

    chunks = create_embeddings(chunks)

    save_knowledge_base(chunks)


# -----------------------------
# Run program
# -----------------------------
if __name__ == "__main__":
    main()