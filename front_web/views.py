
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(response):
    return render(response, "front_web/home.html", {})


def pricing(response):
    return render(response, "front_web/pricing.html", {})


def about(response):
    return render(response, "front_web/about.html", {})


def demo(response):
    return render(response, "front_web/demo.html", {})


def contact(response):
    return render(response, "front_web/contact.html", {})
