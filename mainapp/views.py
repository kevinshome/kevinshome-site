# mainapp/views.py
import os
from urllib.error import HTTPError, URLError
from urllib.request import urlopen
from http.client import HTTPResponse
from django.http import HttpResponse

def index(request):
    return HttpResponse(
        "Welcome to the personal website for kevinshome!<br>"
        "There's really not much here rn <br>"
        "Check back later!"
    )

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
    except URLError as err:
        if isinstance(err.args[0], ConnectionRefusedError):
            response = HttpResponse(
                "<h1>503 Service Unavailable</h1>"
                "csrv is down; contact webmaster"
            )
            response.status_code = 503
            return response
        raise err
    file_data = csrv_request.read()
    response = HttpResponse(file_data)
    response["Content-Type"] = csrv_request.headers["Content-Type"]
    response["Content-Length"] = csrv_request.headers["Content-Length"]
    response["Last-Modified"] = csrv_request.headers["Last-Modified"]
    return response