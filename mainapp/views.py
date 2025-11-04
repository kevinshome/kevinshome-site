# mainapp/views.py
import os
from urllib.error import HTTPError, URLError
from urllib.request import urlopen
import requests
from http.client import HTTPResponse
from django.http import HttpResponse
from django.shortcuts import render
from .quotes import QUOTES

def index(request):
    response_obj = render(request, "index.htm", {})
    response_obj.headers["X-This-Car-Kicks-Ass"] = "and-i-can-watch-madagascar-while-im-driving"
    return response_obj

def upload(request):
    return render(request, "upload.htm", {"password": os.environ['KH_CSRV_UPLOAD_PASSWORD'], "csrv_upload_url": f"{os.environ['KH_CSRV_URL']}/upload", "redirect_url": request.build_absolute_uri('/').strip("/")})

def quotes_page(request):
    return render(request, "quotes.htm", {"quotes": QUOTES})

def list_files(request):
    res = requests.get(os.environ["KH_CSRV_URL"] + '/list')
    return render(request, "filelist.htm", {"file_list": res.json()['file_list']})

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
