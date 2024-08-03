import asyncio
import aiofiles

async def hex_to_pdf(hex_input_path, pdf_output_path):
    async with aiofiles.open(hex_input_path, 'r') as hex_file:
        hex_content = await hex_file.read()
    pdf_content = bytes.fromhex(hex_content)

    async with aiofiles.open(pdf_output_path, 'wb') as pdf_file:
        await pdf_file.write(pdf_content)

async def main():
    hex_input_path = 'PATH_TO_HEXDATA.txt'  # Replace with your actual hex file path
    pdf_output_path = 'restored_output.pdf'  # Path for the restored PDF file

    await hex_to_pdf(hex_input_path, pdf_output_path)
    print(f"Hex content converted back to PDF and saved to {pdf_output_path}")

if __name__ == "__main__":
    asyncio.run(main())
