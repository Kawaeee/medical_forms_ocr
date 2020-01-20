# Medical Forms OCR
- This project is a part of CSC491 Intelligent System and Application Class.

- It is a web application that allows the user to upload PDF/JPG to extracting the paper-based medical form data into a digital medical form.

Documentation link : [Medical Forms OCR report](https://github.com/Kawaeee/medical_forms_ocr/blob/master/report.pdf)

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
 - In order to improve OCR accuracy, it requires better quality of the form 
 - Require to locate each bounding box manually
