from flask import Blueprint, render_template,Response
from cvtest import Video

views = Blueprint('views', __name__)
capture = Video()
capture.start()

@views.route('/')
def setting():
    return render_template("base.html")

@views.route('/api/scan', methods=['GET'])
def scan():
    #capture = video()
    capture.read()
    #capture.read()
    print("scan")
    return Response(response="success", status=200, mimetype="application/json")

@views.route('/api/close', methods=['GET'])
def close():
    #capture = video()
    #capture.start()
    capture.close()

    return Response(response="success", status=200, mimetype="application/json")