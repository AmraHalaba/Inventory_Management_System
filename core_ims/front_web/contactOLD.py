def index(request):
    services       = Service.objects.all()
    pricing_plans  = PricingPlan.objects.all()
    pricing_properties = PricingPlanProperty.objects.all( )
    
    # Contact Form
    if request.method == "POST":
        message_name  = request.POST['message-name']
        message_email = request.POST['message-email']
        message_text  = request.POST['message-text']
        
        send_mail('Message From: ' + message_name,
                  message_text,
                  message_email,
                  ['ims.keeptrack@gmail.com'],
                  fail_silently=False)
        messages.success(request, f'{message_name}, we received your message and will reach back in short notice.')  
    else:
        context = {}
        return render (request, 'front_web/index.html', context)
    
    
    context = { 'services'     : services,
               'pricing_plans' : pricing_plans,
               'pricing_properties' : pricing_properties,
               'message_name'  : message_name,
                   'message_email' : message_email,
                   'message_text'  : message_text}
    return render (request, 'front_web/index.html', context)





<form method="POST" class="contact-form" >
                {% csrf_token %}
                  <div class="wrapper-flex">
                    <div class="input-wrapper">
                      <label for="name">Name*</label>
                      
                      <input type="text" name="message-name" id="name" required placeholder="Enter Your Name" class="input-field">
                    </div>
                    <div class="input-wrapper">
                      <label for="emai">Email*</label>

                      <input type="text" name="message-email" id="email" required placeholder="Enter Your Email"
                        class="input-field">
                    </div>
                  </div>

                  <label for="message">Message*</label>
                  <textarea name="message-text" id="message" required placeholder="Type Your Message"
                    class="input-field"></textarea>

                  <button type="submit" class="btn btn-primary"><span>Send Message</span></button>
              </form>