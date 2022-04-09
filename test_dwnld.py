from flask import send_file, render_template, Flask

app = Flask(__name__, template_folder="html_templates", static_folder="static_content" )

@app.route('/')
def file_downloads():
    try:
        return render_template('downloads.html')
    except Exception as e:
        return str(e) 

@app.route('/return-files/')
def return_files_tut():
	try:
		return send_file('E:\Programms Codes\File_Senior\CONV_RESULTS\Белки являются наиболее сложными веществами организма и основой протоплазмы клеток.docx', attachment_filename='Белки являются наиболее сложными веществами организма и основой протоплазмы клеток.docx')
	except Exception as e:
		return str(e)


if __name__ == '__main__':
    app.run()
    """port=8080, host='127.0.0.1'"""