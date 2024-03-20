# Data Extraction From JEE Admit Cards
It is designed to extract textual information from images and PDF documents using OCR technique. The system employs various image processing and text extraction algorithms to retrieve relevant data from input files. Below is an overview of the functionalities and components of the system:

## Functionality
The primary functionalities of the system include:

Text Extraction from Images: Extracts textual information from image files (.png, .jpg, .jpeg).
Text Extraction from PDFs: Extracts textual information from PDF documents.
Data Retrieval: Extracts specific details such as application numbers, dates of birth, roll numbers, and candidate names from the extracted text.
Error Handling: Includes mechanisms to handle errors gracefully, such as when the OCR process fails or when invalid input files are provided.

## Components
The system consists of the following components:

Image Processing Module: Utilizes OpenCV and other image processing libraries to preprocess images and enhance text extraction accuracy. Techniques such as thresholding, contour detection, and morphological operations are employed to improve the quality of the input images.
OCR Engine: Utilizes the Tesseract OCR engine to perform text recognition on the preprocessed images. Tesseract is configured to recognize text in English language using the eng language model.
Text Extraction Functions: Includes functions to extract specific details such as application numbers, dates of birth, roll numbers, and candidate names from the OCR output. Regular expressions and string manipulation techniques are used to parse the extracted text and retrieve relevant information.
Error Handling Mechanisms: Implements error handling mechanisms to manage failures during the OCR process. This includes handling cases where the input file format is not supported or when the OCR engine fails to extract text accurately.

## Usage
To use the system, follow these steps:

Provide input files: Input files can be either image files (in .png, .jpg, or .jpeg format) or PDF documents.
Execute the appropriate function: Depending on the input file format, use either text_details_jpg() function for images or text_details() function for PDFs to extract text details.
Retrieve extracted information: Extracted information such as application numbers, dates of birth, roll numbers, and candidate names will be returned as output.

## Requirements
The system requires the following dependencies to be installed:

Python 3.x
OpenCV
NumPy
Pillow (PIL)
pytesseract
pdf2image
pandas

Note:- Ensure that Tesseract OCR engine is installed and configured correctly. The path to the Tesseract executable should be specified in the path_to_tesseract variable.
