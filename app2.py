import gradio as gr
from pypdf import PdfReader
import ocrmypdf
from markdownify import markdownify as md


def extract_text_from_pdf(reader):
    full_text = ""
    for idx, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            markdown_text = md(text)  # Convert extracted text to Markdown
            full_text += f"---- Page {idx + 1} ----\n{markdown_text}\n\n"

    return full_text.strip()


def convert(pdf_file):
    try:
        reader = PdfReader(pdf_file)

        # Extract and convert text to Markdown
        full_text = extract_text_from_pdf(reader)

        # Check if there are any images
        image_count = sum(len(page.images) for page in reader.pages)

        # If there are images and not much content, perform OCR on the document
        if image_count > 0 and len(full_text) < 1000:
            out_pdf_file = pdf_file.replace(".pdf", "_ocr.pdf")
            ocrmypdf.ocr(pdf_file, out_pdf_file, force_ocr=True)

            # Re-read the OCR-processed PDF
            reader = PdfReader(out_pdf_file)
            full_text = extract_text_from_pdf(reader)

        return full_text

    except Exception as e:
        return f"An error occurred: {str(e)}", {}


# Launch Gradio interface
gr.Interface(
    convert,
    inputs=[
        gr.File(label="Upload PDF", type="filepath"),
    ],
    outputs=[
        gr.Markdown(label="Extracted Markdown"),  # Output as Markdown for proper formatting
    ],
).launch()
