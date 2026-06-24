# mainapp/views.py
import os
import pyotp
import magic
from django.http import FileResponse, HttpResponse
from django.shortcuts import render, redirect
from .quotes import QUOTES
from .s3_utils import _s3_list_bucket, _s3_dl2ibuf

def index(request):
    response_obj = render(request, "index.htm", {'is_logged_in': request.COOKIES.get('logged_in')})
    response_obj.headers["X-This-Car-Kicks-Ass"] = "https://www.youtube.com/watch?v=VvVThrMhnuE"
    response_obj.headers["X-Economics"] = "https://www.youtube.com/watch?v=ZWjlUsKiyCY&t=54s"
    return response_obj

def upload(request):
    if request.COOKIES.get('logged_in') is None:
        return HttpResponse('<h1>You need to be logged in to upload!</h1><a href="/">Go Home</a>')
    return render(request, "upload.htm", {})

def logout(_):
    res = redirect('/')
    res.delete_cookie('logged_in')
    return res

def login(request):
    if request.COOKIES.get('logged_in') == 'true':
        return redirect('/')

    if request.method == "POST":
        totp = pyotp.TOTP(os.environ["OTP_KEY"])
        if request.POST['passcode'] == totp.now():
            response = redirect('/')
            response.set_cookie(
                'logged_in',
                'true', 
                max_age=86400
            )
        else:
            response = redirect('/login?fail=1')
        return response
    else:
        if request.GET.get('fail') is not None:
            print('failed')
        return render(request, "login.htm", {})

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
