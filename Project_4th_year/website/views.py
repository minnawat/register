from flask import Blueprint, render_template,Response
from cvtest import video,finder,search_send
import socket

views = Blueprint('views', __name__)


@views.route('/')
def setting():
    return render_template("base.html")

@views.route('/api/test', methods=['GET'])
def test():
    capture = video()
    capture.run()
    search = search_send()
    search.run()

    return Response(response="success", status=200, mimetype="application/json")