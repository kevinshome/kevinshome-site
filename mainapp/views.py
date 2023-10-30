# mainapp/views.py
from datetime import datetime

from django.http import HttpResponse

def index(request):
    return HttpResponse(f"\"{request.build_absolute_uri('/').strip('/')}\"<br>GET /")