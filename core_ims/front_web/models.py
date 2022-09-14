from django.db import models
from tabnanny import verbose


class Service(models.Model):
    # Basic Fields
    title                      = models.CharField(max_length=200)
    short_description          = models.TextField(max_length=500)
    detailed_description_line1 = models.TextField(max_length=1000, null=True, blank=True)
    detailed_description_line2 = models.TextField(max_length=1000, null=True, blank=True)
    detailed_description_line3 = models.TextField(max_length=1000, null=True, blank=True)
    detailed_description_line4 = models.TextField(max_length=1000, null=True, blank=True)
    detailed_description_line5 = models.TextField(max_length=1000, null=True, blank=True)
    service_photo              = models.ImageField(default='default_service.png', null=True, blank=True, upload_to='service_images')
    
    # Utility Fields
    date_created                = models.DateTimeField(auto_now_add=True)
    date_updated                = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title


class PricingPlanProperty(models.Model):
    # Basic Fields
    property = models.CharField(max_length=50)
    
    # Utility Fields
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'pricing plan property'
        verbose_name_plural = 'pricing plan properties'
        
    def __str__(self):
        return self.property


class PricingPlan(models.Model):
    # Basic Fields
    title       = models.CharField(max_length=50)
    price       = models.FloatField(default=0.00)
    description = models.CharField(max_length=200, null=True)
    
    # Related Fields 
    properties  = models.ManyToManyField(PricingPlanProperty, null=True)
    
    # Utility Fields
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
        
    def all_properties(self):
        voting = PricingPlanProperty.objects.filter(property=self)
        return voting