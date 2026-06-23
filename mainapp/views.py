# mainapp/views.py
import os
import magic
from django.http import FileResponse
from django.shortcuts import render
from .quotes import QUOTES
from .s3_utils import _s3_list_bucket, _s3_dl2ibuf

def index(request):
    response_obj = render(request, "index.htm", {})
    response_obj.headers["X-This-Car-Kicks-Ass"] = "https://www.youtube.com/watch?v=VvVThrMhnuE"
    response_obj.headers["X-Economics"] = "https://www.youtube.com/watch?v=ZWjlUsKiyCY&t=54s"
    return response_obj

def upload(request):
    return render(request, "upload.htm", {"password": os.environ['KH_CSRV_UPLOAD_PASSWORD'], "csrv_upload_url": f"{os.environ['KH_CSRV_URL']}/upload", "redirect_url": request.build_absolute_uri('/').strip("/")})

def quotes_page(request):
    return render(request, "quotes.htm", {"quotes": QUOTES})

def list_files(request):
    items = _s3_list_bucket()
    return render(request, "filelist.htm", {"file_list": items})

def get_file(_, path):
    filebuf = _s3_dl2ibuf(path)
    mimetype = magic.from_buffer(filebuf.read(2048), mime=True)
    filebuf.seek(0)
    res = FileResponse(
        filebuf,
        as_attachment=False,
        content_type=mimetype,
    )
    return res
