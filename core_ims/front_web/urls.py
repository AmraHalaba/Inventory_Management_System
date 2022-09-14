from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views as views

urlpatterns = [
    path('', views.index, name="index"),
    path('single_service/<str:pk>/', views.single_service, name="single_service"), 
    path('/', views.contact, name="contact"), 
    path('search_bar', views.search_bar, name="search_bar"), 
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)