from flask import Blueprint, render_template,Response
from cvtest import video,finder
import socket

views = Blueprint('views', __name__)


@views.route('/')
def setting():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    data = {'hostname': hostname, 'local_ip': local_ip}
    return render_template("base.html",data=data)

@views.route('/api/test', methods=['GET'])
def test():
    capture = video()
    capture.run()

    return Response(response="success", status=200, mimetype="application/json")