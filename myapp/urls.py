from django.urls import path
from .views import index, upload, download

urlpatterns = [
	path('', index, name='index'),
	path('upload/', upload, name='upload'),
	path('download/', download, name='download'),
]