# mainapp/urls.py
from django.urls import path

from mainapp.views import index, get_file, upload, list_files, quotes_page, login, logout


urlpatterns = (
    path('', index),
    path('files/', list_files),
    path('files/<str:path>', get_file),
    path('upload/', upload),
    path('login/', login),
    path('logout/', logout),
    path('quotes/', quotes_page),
)