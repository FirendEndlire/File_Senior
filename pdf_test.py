import requests
import json

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
  with open('result.pdf', 'wb') as fd:
    for chunk in response.iter_content(chunk_size=8096):
      fd.write(chunk)
else:
  print(response.text)
  exit()