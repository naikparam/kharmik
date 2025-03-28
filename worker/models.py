from django.db import models

# Create your models here.
from django.db import models

class Farmer(models.Model):  
    aadhar = models.CharField(primary_key=True, max_length=12)  # Aadhar is usually a 12-digit string  
    phone_number = models.CharField(max_length=15)  # Phone numbers are best stored as strings  
    name = models.CharField(max_length=100)  # Name should be a string  
    date_of_start = models.DateField()  # Date field for storing dates  
    crop_type = models.CharField(max_length=100)   # Boolean for binary choices  
    image = models.ImageField(upload_to='images/', null=True, blank=True)  
      # Photo can be a URL or base64 encoded data  

    def __str__(self):  
        return self.name  
class Crop(models.Model):
    farmer_aadhar =  models.ForeignKey('farmer',max_length=12, on_delete=models.CASCADE)   # Aadhar ID of the farmer
    worker_aadhar = models.ForeignKey('Worker',max_length=12, on_delete=models.CASCADE)  # Reference to Worker model via Aadhar
    crop_name = models.CharField(max_length=100)  # Crop name
    working_date = models.DateField()  # Date of worker's activity on the crop
    per_day_price = models.DecimalField(max_digits=10, decimal_places=2)  # Daily price for the worker

    def __str__(self):
        return f"{self.crop_name} - {self.farmer_aadhar} - {self.worker_aadhar}"
    
class Worker(models.Model):  
    aadhar = models.CharField(primary_key=True, max_length=12)  # Aadhar is a 12-digit string  
    phone_number = models.CharField(max_length=15)  # Phone number stored as string  
    name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)   # Worker’s name   # Date of joining  
    job_type = models.CharField(max_length=100)  # Type of work  
    image = models.ImageField(upload_to='worker_images/', null=True, blank=True)  # Profile picture  

    def __str__(self):  
        return self.name 
