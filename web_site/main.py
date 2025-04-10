from flask import Flask, url_for, request, render_template, redirect


app = Flask(__name__)
k = ''
app.config['SECRET_KEY'] = 'universe_site_Akim_and_Val_secret_key'


@app.route('/ap')
def pr():
    return render_template('main_window.html')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
