from __future__ import unicode_literals 
from django.db import models 

class ContactForm(models.Model):
    
    
    name = models.CharField(max_length =20) 
    email = models.CharField(max_length =20) 
    txt = models.TextField(max_length =20) 

    def __str__(self):
        return self.set_name 
        
