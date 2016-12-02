from flask import Flask, render_template, request, session, url_for, redirect

from utils import content

app = Flask(__name__)
app.secret_key = "secrets"

@app.route("/")
def root():
    return render_template('home.html')

if __name__ == "__main__":
    app.debug = True
    app.run()
