from flask import Blueprint, render_template,Response
from cvtest import capture

views = Blueprint('views', __name__)


@views.route('/')
def setting():
    return render_template("base.html")

@views.route('/api/scan', methods=['GET'])
def scan():
    #capture = video()
    #capture.start()
    capture.search_send()

    return Response(response="success", status=200, mimetype="application/json")

@views.route('/api/close', methods=['GET'])
def close():
    #capture = video()
    #capture.start()
    capture.close()

    return Response(response="success", status=200, mimetype="application/json")