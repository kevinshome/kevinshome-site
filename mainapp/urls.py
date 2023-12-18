# mainapp/urls.py
from django.urls import path

from mainapp.views import index, get_file, upload


urlpatterns = [
    path('', index),
    path('files/<str:path>', get_file),
    path('upload/', upload),
]