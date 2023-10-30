# mainapp/views.py
import os
from urllib.error import HTTPError
from urllib.request import urlretrieve
from django.http import HttpResponse

def index(request):
    return HttpResponse(f"\"{request.build_absolute_uri('/').strip('/')}\"<br>GET /")

def get_file(_, path):
    try:
        file_loc, file_headers = urlretrieve(os.environ["KH_CSRV_URL"] + f'/{path}', "dl_out")
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
    file_data = None
    with open(file_loc, 'rb') as f:
        file_data = f.read()
    os.remove(file_loc)
    response = HttpResponse(file_data)
    response["Content-Type"] = file_headers["Content-Type"]
    response["Content-Length"] = file_headers["Content-Length"]
    return response