import gradio as gr
from pypdf import PdfReader
import ocrmypdf


def extract_text_from_pdf(reader):
    full_text = ""
    for idx, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:  # Avoid checking len(text) > 0 explicitly
            full_text += f"---- Page {idx + 1} ----\n{text}\n\n"  # Adjust page numbering

    return full_text.strip()


def convert(pdf_file):
    try:
        reader = PdfReader(pdf_file)

        # Extract text
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
        gr.Textbox(label="Markdown"),  # Change output to Textbox for better markdown display
    ],
).launch()
