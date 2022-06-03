from django.urls import path
from . import views as views

urlpatterns = [
    path('', views.home, name="homepage"),
    path('pricing/', views.pricing, name='pricingpage'),
    path('about/', views.about, name='aboutpage'),
    path('demo/', views.demo, name='demopage'),
    path('contact/', views.contact, name='contactpage'),
]
