from django.urls import path
from .views import index, login, documentsList, scraper
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
	path('', index, name='index'),
	path('login/', login, name='login'),	
	path('docs/', documentsList.as_view(), name='docs_list'),
	path('scraper/', scraper, name='scrape'),
]