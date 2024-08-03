import os
import sys
import math
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QFileDialog
from PyPDF2 import PdfReader
import subprocess

# Function to convert PDF file to binary data split into chunks
def convert_pdf_to_binary(pdf_file_path, max_size_mb=1):
    # Determine chunk size in bytes
    max_size_bytes = max_size_mb * 1024 * 1024

    # Open the PDF file
    with open(pdf_file_path, 'rb') as pdf_file:
        pdf_reader = PdfReader(pdf_file)
        total_pages = len(pdf_reader.pages)  # Get total number of pages

        # List to hold binary data chunks
        binary_chunks = []

        current_chunk = ''  # Initialize current chunk
        current_chunk_size = 0  # Initialize current chunk size

        # Read PDF page by page
        for page_num in range(total_pages):
            page = pdf_reader.pages[page_num]
            page_content = page.extract_text()  # Extract text
            page_size = len(page_content)

            # Iterate through each character in the page content
            for char in page_content:
                binary_char = bin(ord(char))[2:].zfill(8)  # Convert character to binary string
                current_chunk += binary_char
                current_chunk_size += len(binary_char)

                # Check if adding this character would exceed max_size_bytes
                if current_chunk_size >= max_size_bytes:
                    binary_chunks.append(current_chunk)
                    current_chunk = ''
                    current_chunk_size = 0

        # Append the last chunk if it's not empty
        if current_chunk:
            binary_chunks.append(current_chunk)

    return binary_chunks

class PDFConverterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('PDF Converter')
        self.setGeometry(100, 100, 400, 200)

        self.file_path = None
        self.progress_label = QLabel('Select a PDF file or folder')
        self.progress_label.setAlignment(Qt.AlignCenter)

        self.select_button = QPushButton('Select File or Folder', self)
        self.select_button.clicked.connect(self.select_file)

        self.convert_button = QPushButton('Convert', self)
        self.convert_button.clicked.connect(self.convert_pdf)

        self.output_button = QPushButton('Open Output Folder', self)
        self.output_button.clicked.connect(self.open_output_folder)
        self.output_button.setEnabled(False)

        vbox = QVBoxLayout()
        vbox.addWidget(self.progress_label)
        vbox.addWidget(self.select_button)
        vbox.addWidget(self.convert_button)
        vbox.addWidget(self.output_button)

        self.setLayout(vbox)

    def select_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setNameFilter('PDF files (*.pdf)')
        if file_dialog.exec_():
            self.file_path = file_dialog.selectedFiles()[0]
            self.progress_label.setText(f'Selected: {self.file_path}')
            self.output_button.setEnabled(True)

    def convert_pdf(self):
        if self.file_path:
            # Convert PDF to binary data
            binary_chunks = convert_pdf_to_binary(self.file_path)

            # Create a folder to store binary text files
            output_folder = os.path.join(os.path.dirname(self.file_path), 'binary_data')
            os.makedirs(output_folder, exist_ok=True)

            # Save each binary chunk to a separate text file
            for idx, chunk in enumerate(binary_chunks):
                chunk_filename = os.path.join(output_folder, f'chunk_{idx + 1}.txt')
                with open(chunk_filename, 'w') as file:
                    file.write(chunk)

            print(f'Saved {len(binary_chunks)} binary chunks to {output_folder}')

    def open_output_folder(self):
        # Open the folder containing the converted output files
        if self.file_path:
            output_folder = os.path.join(os.path.dirname(self.file_path), 'binary_data')
            if sys.platform.startswith('win'):
                os.startfile(output_folder)  # Opens folder in Windows File Explorer
            elif sys.platform.startswith('darwin'):
                subprocess.call(['open', '--', output_folder])  # Opens folder in macOS Finder
            elif sys.platform.startswith('linux'):
                subprocess.call(['xdg-open', '--', output_folder])  # Opens folder in Linux file manager


if __name__ == '__main__':
    app = QApplication(sys.argv)
    converter = PDFConverterApp()
    converter.show()
    sys.exit(app.exec_())
