import os
import sys
import math
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QFileDialog, QLineEdit, QMessageBox, QCheckBox
import subprocess
import multiprocessing
import io
import fitz  # PyMuPDF

# Function to convert PDF file to binary data split into chunks using PyMuPDF for page-wise processing
def convert_pdf_to_binary_pymupdf(pdf_file_path, max_size_mb=1, max_pages=None):
    max_size_bytes = max_size_mb * 1024 * 1024
    binary_chunks = []

    try:
        doc = fitz.open(pdf_file_path)
    except Exception as e:
        QMessageBox.critical(None, "Error", f"Failed to open PDF file: {str(e)}")
        return [] 
    
    total_pages = min(doc.page_count, max_pages) if max_pages else doc.page_count

    current_chunk = ''
    current_chunk_size = 0

    for page_num in range(total_pages):
        page = doc.load_page(page_num)
        page_text = page.get_text()
        
        for char in page_text:
            binary_char = bin(ord(char))[2:].zfill(8)
            current_chunk += binary_char
            current_chunk_size += len(binary_char)

            if current_chunk_size >= max_size_bytes:
                binary_chunks.append(current_chunk)
                current_chunk = ''
                current_chunk_size = 0

    if current_chunk:
        binary_chunks.append(current_chunk)

    doc.close()
    return binary_chunks

# Function to convert PDF file to binary data split into chunks using streaming approach
def convert_pdf_to_binary_stream(pdf_file_path, chunk_size=1024):
    binary_chunks = []

    with open(pdf_file_path, 'rb') as pdf_file:
        while True:
            chunk = pdf_file.read(chunk_size)
            if not chunk:
                break

            for byte in chunk:
                binary_char = bin(byte)[2:].zfill(8)
                binary_chunks.append(binary_char)

    return binary_chunks

# Worker class for processing PDF files in a separate thread
class PDFProcessor(QThread):
    finished = pyqtSignal()

    def __init__(self, pdf_files, use_pymupdf, max_size_mb, max_pages=None):
        super().__init__()
        self.pdf_files = pdf_files
        self.use_pymupdf = use_pymupdf
        self.max_size_mb = max_size_mb
        self.max_pages = max_pages

    def run(self):
        try:
            for pdf_file in self.pdf_files:
                if self.use_pymupdf:
                    binary_chunks = convert_pdf_to_binary_pymupdf(pdf_file, self.max_size_mb, self.max_pages)
                else:
                    binary_chunks = convert_pdf_to_binary_stream(pdf_file)

                # Process or save binary_chunks as needed
                print(f'Processed {pdf_file}')

            self.finished.emit()
        except Exception as e:
            print(f'Error in PDFProcessor: {str(e)}')
        finally:
            self.quit()  # Quit the thread loop
            self.wait()  # Wait for the thread to finish

class PDFConverterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('PDF Converter')
        self.setGeometry(100, 100, 400, 250)

        self.file_path = None
        self.folder_path = None

        self.progress_label = QLabel('Select a PDF file or folder')
        self.progress_label.setAlignment(Qt.AlignCenter)

        self.select_file_button = QPushButton('Select File', self)
        self.select_file_button.clicked.connect(self.select_file)

        self.select_folder_button = QPushButton('Select Folder', self)
        self.select_folder_button.clicked.connect(self.select_folder)

        self.pages_label = QLabel('Max Pages:')
        self.pages_input = QLineEdit(self)
        self.pages_input.setPlaceholderText('Enter max pages (optional)')

        self.size_label = QLabel('Max Size (MB):')
        self.size_input = QLineEdit(self)
        self.size_input.setPlaceholderText('Enter max size in MB')

        self.use_pymupdf_checkbox = QCheckBox('Use PyMuPDF (page-wise processing)')
        self.use_pymupdf_checkbox.setChecked(True)

        self.convert_button = QPushButton('Convert', self)
        self.convert_button.clicked.connect(self.convert_pdf)
        self.convert_button.setEnabled(False)

        self.output_button = QPushButton('Open Output Folder', self)
        self.output_button.clicked.connect(self.open_output_folder)
        self.output_button.setEnabled(False)

        vbox = QVBoxLayout()
        vbox.addWidget(self.progress_label)
        vbox.addWidget(self.select_file_button)
        vbox.addWidget(self.select_folder_button)
        vbox.addWidget(self.pages_label)
        vbox.addWidget(self.pages_input)
        vbox.addWidget(self.size_label)
        vbox.addWidget(self.size_input)
        vbox.addWidget(self.use_pymupdf_checkbox)
        vbox.addWidget(self.convert_button)
        vbox.addWidget(self.output_button)

        self.setLayout(vbox)

    def select_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter('PDF files (*.pdf)')
        if file_dialog.exec_():
            self.file_path = file_dialog.selectedFiles()[0]
            self.progress_label.setText(f'Selected File: {self.file_path}')
            self.convert_button.setEnabled(True)
            self.output_button.setEnabled(False)

    def select_folder(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        folder_dialog = QFileDialog()
        folder_dialog.setFileMode(QFileDialog.Directory)
        folder_dialog.setOption(QFileDialog.ShowDirsOnly, True)
        if folder_dialog.exec_():
            self.folder_path = folder_dialog.selectedFiles()[0]
            self.progress_label.setText(f'Selected Folder: {self.folder_path}')
            self.convert_button.setEnabled(True)
            self.output_button.setEnabled(False)


    def convert_pdf(self):
        max_pages = int(self.pages_input.text()) if self.pages_input.text().strip().isdigit() else None
        max_size_mb = int(self.size_input.text()) if self.size_input.text().strip().isdigit() else 1
        use_pymupdf = self.use_pymupdf_checkbox.isChecked()

        if self.file_path:
            pdf_files = [self.file_path]
        elif self.folder_path:
            pdf_files = []
            for root, _, files in os.walk(self.folder_path):
                for file in files:
                    if file.endswith('.pdf'):
                        pdf_files.append(os.path.join(root, file))

        if not pdf_files:
            print('No PDF files found.')
            return

        # Start processing in a separate thread
        worker = PDFProcessor(pdf_files, use_pymupdf, max_size_mb, max_pages)
        worker.finished.connect(self.processing_finished)
        worker.start()

        self.convert_button.setEnabled(False)
        self.output_button.setEnabled(False)

    def processing_finished(self):
        self.convert_button.setEnabled(True)
        self.output_button.setEnabled(True)
        print('Conversion finished.')
        
        
    def open_output_folder(self):
        if self.folder_path:
            output_folder = os.path.join(self.folder_path, 'binary_data')
            if sys.platform.startswith('win'):
                os.startfile(output_folder)
            elif sys.platform.startswith('darwin'):
                subprocess.call(['open', '--', output_folder])
            elif sys.platform.startswith('linux'):
                subprocess.call(['xdg-open', '--', output_folder])

if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    converter = PDFConverterApp()
    converter.show()
    sys.exit(app.exec_())

