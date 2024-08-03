import asyncio
import aiofiles

async def pdf_to_hex(pdf_path, hex_output_path):
    async with aiofiles.open(pdf_path, 'rb') as pdf_file:
        pdf_content = await pdf_file.read()
    hex_content = pdf_content.hex()

    async with aiofiles.open(hex_output_path, 'w') as hex_file:
        await hex_file.write(hex_content)

async def main():
    pdf_path = 'PATH_TO_PDF_FILE.pdf'  # Replace with your actual PDF file path
    hex_output_path = 'output_hex.txt'  # Path for the hex file output

    await pdf_to_hex(pdf_path, hex_output_path)
    print(f"PDF content converted to hex and saved to {hex_output_path}")

if __name__ == "__main__":
    asyncio.run(main())
