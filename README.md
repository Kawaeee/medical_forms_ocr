# Medical Forms OCR
- This project is a part of CSC491 Intelligent System and Application Class

- It is web application that allow user to uploading PDF/JPG to extracting the paper-based medical form data into a digital medical form.

Documentation link : -

## Installation

- Install pytesseract and poppler, make sure you include both of them into PATH

    - https://github.com/tesseract-ocr/tesseract/wiki
    - https://pypi.org/project/pdf2image/
    
- Install dependencies
    ```Bash
    pip install -r requirements.txt
    ```
- Run Flask website python script and access it using your IP at port 5000
    ```Bash
    python main.py 
    ```
  
## Limitations
 - Focus only Infliximab form
 - Require better quality of the form in order to improve OCR accuracy
 - Require locate each bbox manually
