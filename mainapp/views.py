# mainapp/views.py
import os
from urllib.error import HTTPError
from urllib.request import urlopen
from http.client import HTTPResponse
from django.http import HttpResponse

def index(request):
    return HttpResponse(f"\"{request.build_absolute_uri('/').strip('/')}\"<br>GET /")

def get_file(_, path):
    try:
        csrv_request: HTTPResponse = urlopen(os.environ["KH_CSRV_URL"] + f'/{path}')
    except HTTPError as err:
        if err.code == 404:
            response = HttpResponse("<h1>404 File Not Found</h1>")
            response.status_code = 404
            return response
        else:
            response = HttpResponse(
                "<h1>502 Bad Gateway</h1>"
                f"got {err.code} from csrv; contact webmaster"
            )
            response.status_code = 502
            return response
    file_data = csrv_request.read()
    response = HttpResponse(file_data)
    response["Content-Type"] = csrv_request.headers["Content-Type"]
    response["Content-Length"] = csrv_request.headers["Content-Length"]
    return response