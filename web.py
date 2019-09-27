from flask import Flask, render_template, request
from main import *

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html', status="good")


@app.route("/graphics")
def graphics():
    return render_template('/graphics/void_dweller.png', status="good")


@app.route("/busInfo")
def busInfo():
    postcode = request.args.get('postcode').upper()
    data = main(postcode)

    if data == 404:
        return render_template('index.html', status="bad")

    return render_template('info.html', postcode=postcode, data=data)

if __name__ == "__main__": app.run()