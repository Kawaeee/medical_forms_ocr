# Flask
from flask import Flask, render_template,request,redirect,url_for,send_file
from werkzeug.utils import secure_filename

# PDF
from pdf2image import convert_from_path,convert_from_bytes
import os 
import sys 

# PDF creator
from fpdf import FPDF

# Pillow (Image)
from PIL import Image,ImageFilter,ImageEnhance,ImageDraw

# OCR
import pytesseract 

UPLOAD_FOLDER = os.path.join('static/')

app = Flask(__name__,static_url_path='/static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/extract',methods = ['POST'])
def extract_pdf():
    data = request.files['file']

    if(data.filename == ''):
        return render_template('index.html',msg='Your uploaded file is null!!')

    extension = data.filename.split('.')
    if(extension[-1].lower() == 'pdf'):
        print('PDF')
        page = convert_from_bytes(data.read())
        full_filename = os.path.join(app.config['UPLOAD_FOLDER'], extension[0]+'.jpg')
        img = page[0]
        img.save(full_filename,'JPEG')

    else:
        print('Images')
        img = Image.open(data)
        filename = secure_filename(data.filename)
        full_filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        img.save(full_filename,'JPEG')

    form_type_img = img.crop((1064, 180, 1353, 243))
    form_medicine_img = img.crop((855, 181, 976, 234))
        
    form_type = pytesseract.image_to_string(form_type_img)
    form_medicine = pytesseract.image_to_string(form_medicine_img)

    if(form_type.lower().find('ankylosing spondylitis') != -1 and form_medicine.lower().find('infliximab') != -1):
        print('Proceed to form OCR and allow edit')
        ocr_res = extract_anky(img)

    else:
        return render_template('index.html',msg='Currently we did not support this form type!!')

    return render_template('extraction.html',
                            image_name=full_filename,
                            weight = ocr_res[0],
                            date = ocr_res[1],
                            init_bas = ocr_res[2],
                            curr_bas = ocr_res[3],
                            init_ga = ocr_res[4],
                            curr_ga = ocr_res[5],
                            additional = ocr_res[6],
                            )

def export_pdf(post_res):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial','B',size=16)
    # Header
    pdf.cell(200, 10, txt='Approval for using Infliximab in Ankylosing Spondylitis Patient', ln=1, align='C')
    # Body
    pdf.set_font('Arial',size=12)
    
    pdf.cell(200, 10, txt='Weight: '+post_res[0], ln=1, align='C')
    pdf.cell(200, 10, txt='Date of evaluation: '+post_res[1], ln=1, align='C')
    pdf.cell(200, 10, txt='Initial BASDAI: '+post_res[2], ln=1, align='C')
    pdf.cell(200, 10, txt='Current BASDAI: '+post_res[3], ln=1, align='C')
    pdf.cell(200, 10, txt='Initial Physician Global Assessment: '+post_res[4], ln=1, align='C')
    pdf.cell(200, 10, txt='Current Physician Global Assessment: '+post_res[5], ln=1, align='C')
    pdf.cell(200, 10, txt='Additional Information from Doctor: '+post_res[6], ln=1, align='C')  

    pdf.set_author('Kasidech Chumkun')
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'result/sample_form.pdf')
    pdf.output(full_filename)
    return full_filename
    
@app.route('/result',methods = ['POST'])
def downloadFile ():
    weight = request.form.get('weight')
    date = request.form.get('date')
    init_bas = request.form.get('init_bas')
    curr_bas = request.form.get('curr_bas')
    init_ga = request.form.get('init_ga') 
    curr_ga = request.form.get('curr_ga')
    additional = request.form.get('additional')

    post_res = [weight,date,init_bas,curr_bas,init_ga,curr_ga,additional]

    full_filename = export_pdf(post_res)

    return send_file(full_filename, as_attachment=True)

def extract_anky(img):
    # List all bbox that from image
    weight_img = img.crop((502,459,585,499))
    date_img =  img.crop((503,511,589,554))
    init_bas_img = img.crop((676,742,782,783))
    curr_bas_img = img.crop((1169,752,1274,795))
    init_ga_img  = img.crop((824,789,928,832))
    curr_ga_img = img.crop((1395,801,1500,842))
    additional_img  = img.crop((538,1199,1427,1357))

    # Get all value from each bbox
    weight = pytesseract.image_to_string(weight_img,lang='digits1',config=r'--oem 3 --psm 11')
    date = pytesseract.image_to_string(date_img,lang='digits1',config=r'--oem 3 --psm 11')
    init_bas = pytesseract.image_to_string(init_bas_img,lang='digits1',config=r'--oem 3 --psm 13')
    curr_bas = pytesseract.image_to_string(curr_bas_img,lang='digits1',config=r'--oem 3 --psm 11')
    init_ga = pytesseract.image_to_string(init_ga_img,lang='digits1',config=r'--oem 3 --psm 8')
    curr_ga = pytesseract.image_to_string(curr_ga_img,lang='digits1',config=r'--oem 3 --psm 8')
    additional = pytesseract.image_to_string(additional_img,lang='eng',config=r'--oem 3 --psm 8')

    res = [weight,date,init_bas,curr_bas,init_ga,curr_ga,additional]
    return res


app.run(debug=True,host= '0.0.0.0',use_reloader=False)