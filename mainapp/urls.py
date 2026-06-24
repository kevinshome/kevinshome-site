# mainapp/urls.py
from django.urls import path
from django.shortcuts import redirect

from mainapp.views import index, get_file, upload, list_files, quotes_page, login, logout


urlpatterns = [
    path('', index),
    path('files/<str:path>', get_file),
    path('upload/', upload),
    path('login/', login),
    path('logout/', logout),
    path('filelist/', list_files),
    path('quotes/', quotes_page),
]