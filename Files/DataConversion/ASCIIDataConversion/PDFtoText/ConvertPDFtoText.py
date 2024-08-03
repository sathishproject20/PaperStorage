import fitz  # PyMuPDF
import aiofiles
import asyncio

async def extract_text_from_pdf(pdf_path, txt_output_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text()

    async with aiofiles.open(txt_output_path, 'w') as file:
        await file.write(text)

async def main():
    pdf_path = 'Your_PDF_File.pdf'  # Replace with your actual PDF file path
    txt_output_path = 'output.txt'     # Path for the text file output

    await extract_text_from_pdf(pdf_path, txt_output_path)
    print(f"Text extracted and saved to {txt_output_path}")

if __name__ == "__main__":
    asyncio.run(main())
