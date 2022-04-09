from flask import Flask, render_template
app = Flask(__name__, template_folder="html_templates", static_folder="static_content" )


@app.route('/')
@app.route('/start_page')
def start_page():
    return render_template('Start.html')


@app.route('/registration_page')
def registration_page():
    return render_template('Registration.html')


@app.route('/log_in_page')
def log_in_page():
    return render_template('Login.html')


@app.route('/converter_page')
def converter_page():
    return render_template('Converter.html')


if __name__ == '__main__':
    app.run()
    """port=8080, host='127.0.0.1'"""
    
