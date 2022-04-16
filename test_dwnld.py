from flask import send_file, render_template, Flask
import requests
import json

app = Flask(__name__, template_folder="html_templates", static_folder="static_content" )

@app.route('/dwld')
def file_downloads():
    try:
        return render_template('downloads.html')
    except Exception as e:
        return str(e) 

@app.route('/return-files/')
def return_files_tut():
	try:
		return send_file('CONV_RESULTS/DOCUMENT.pdf')
	except Exception as e:
		return str(e)

@app.route('/')
def get_file():
    instructions = {
    'parts': [
        {
        'file': 'document'
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
        'document': open('CONV_MATERIALS/document.docx', 'rb')
    },
    data = {
        'instructions': json.dumps(instructions)
    },
    stream = True
    )

    if response.ok:
        with open('CONV_RESULTS/DOCUMENT.pdf', 'wb') as fd:
            for chunk in response.iter_content(chunk_size=8096):
                fd.write(chunk)
    else:
        print(response.text)
        exit()
    
if __name__ == '__main__':
    app.run()
    """port=8080, host='127.0.0.1'"""
    
