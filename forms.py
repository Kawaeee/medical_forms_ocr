# OS for path locator
import os 

# PDF creator
from fpdf import FPDF

# Pillow (Image)
from PIL import Image

# OCR
import pytesseract 

def export_pdf(post_res):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial','B',size=16)

    pdf.cell(200, 10, txt='Approval for using Infliximab in Ankylosing Spondylitis Patient', ln=1, align='C')

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