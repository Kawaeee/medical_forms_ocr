# Flask
from flask import Flask,render_template,request,send_file
from werkzeug.utils import secure_filename

# PDF
from pdf2image import convert_from_bytes

# Pillow (Image)
from PIL import Image

# OS for path locator
import os 

# Additional functions
import forms

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

# Flask Run
app.run(debug=True,host= '0.0.0.0',use_reloader=False)