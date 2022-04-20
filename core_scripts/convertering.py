import requests
import json
def conv_to_pdf(material_file):
    if material_file.rsplit('.', 1)[1].lower() in ["doc", "docx", "xls", "xlsx", "ppt", "pptx"]:
        file_type_key = "file"
        file_type_value = "document"
        
    elif material_file.rsplit('.', 1)[1].lower() in ["jpg", "png", "tiff", "html"]:
        file_type_key = "file"
        file_type_value = "image"
    elif material_file.rsplit('.', 1)[1].lower() in ["html"]:
        file_type_key = "html"
        file_type_value = "index.html"
    instructions = {
    'parts': [
        {
        file_type_key: file_type_value
        }
    ]
    }

    response = requests.request(
    'POST',
    'https://api.pspdfkit.com/build',
    headers = {
        'Authorization': 'Bearer pdf_live_dPd0J1OVPV0N6aIB2g4i2INCl4ECy3PeHYssXdmoSev'
    },
    files = {
        file_type_value: open("MATERIALS/" + material_file, 'rb')
    },
    data = {
        'instructions': json.dumps(instructions)
    },
    stream = True
    )

    if response.ok:
        with open('CONV_RESULTS/'+material_file.rsplit('.', 1)[0].lower()+'.pdf', 'wb') as fd:
            for chunk in response.iter_content(chunk_size=8096):
                fd.write(chunk)
        return('CONV_RESULTS/'+material_file.rsplit('.', 1)[0].lower()+'.pdf')
    else:
        return("ERROR")
        print(response.text)
        exit()