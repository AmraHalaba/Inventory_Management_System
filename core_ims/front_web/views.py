import email
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from multiprocessing import context
from django.core.mail import send_mail
from django.contrib import messages
# from django.db.models import Q
# from django.core.mail import EmailMessage
# from django.conf import settings
# from django.template.loader import render_to_string

from .models import *
from .forms import *


# Create your views here.


def index(request):
    services       = Service.objects.all()
    pricing_plans  = PricingPlan.objects.all()
    pricing_properties = PricingPlanProperty.objects.all( )
    
    context = { 'services'     : services,
            'pricing_plans' : pricing_plans,
            'pricing_properties' : pricing_properties }
    return render (request, 'front_web/index.html', context)


"""def index(request):
    services           = Service.objects.all()
    pricing_plans      = PricingPlan.objects.all()
    pricing_properties = PricingPlanProperty.objects.all( )
    form               = ContactForm()
    
    # Contact Form
    if request.method == "POST":
        form = ContactForm(request.POST) 
        
        if form.is_valid():
            name    = form.cleaned_data['name']
            email   = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            context = { 'name'    : name,
                        'email'   : email,
                        'message' : message}
            html    = render_to_string('front_web/email_template.html', context)
            
            send_mail('Message From: ' + name,
                      message,
                      email,
                      ['ims.keeptrack@gmail.com'],
                      fail_silently=False,
                      html_message=html)
            messages.success(request, f'{name}, we received your message and will reach back in short notice.') 
            
            return redirect('/')
        else:
            form = ContactForm()
    
    
    context = { 'services'          : services,
               'pricing_plans'      : pricing_plans,
               'pricing_properties' : pricing_properties,
               'form'               : form }
    return render (request, 'front_web/index.html', context)"""


def pricing(request):
    pricing_plans   = PricingPlan.objects.all()
    
    context = { 'pricing_plans' : pricing_plans}
    return render (request, 'front_web/index.html', context)

def contact(request):    
    if request.method == "POST":
        message_name  = request.POST['message-name']
        message_email = request.POST['message-email']
        message_text  = request.POST['message-text']
        
        send_mail('Message From: ' + message_name,
                  message_text,
                  message_email,
                  ['ims.keeptrack@gmail.com'],
                  fail_silently=False)
                
        context = {'message_name'  : message_name,
                   'message_email' : message_email,
                   'message_text'  : message_text}
        messages.success(request, f'{message_name}, we received your message and will reach back in short notice.')
        return render (request, 'front_web/index.html', context)
        #return redirect('/')
    else:
        #context = {}
        #return render (request, 'front_web/index.html', context)
        messages.error(request, 'There was an error. Please try again.')
        return redirect('/')



def single_service(request, pk):
    service_details = Service.objects.filter(id=pk)
    
    context = { 'service_details' : service_details }
    return render (request, 'front_web/single_service.html', context)



def search_bar(request):
    if request.method == "POST":
        search_query = request.POST['search-query']
        services     = Service.objects.filter(title__icontains=search_query)
        
        context = { 'search_query' : search_query,
                    'services'     : services}
        return render (request, 'front_web/search_services.html', context)
    else:
        context = {}
        return render (request, 'front_web/search_services.html', context)
    
