from __future__ import unicode_literals 
from django.db import models 

class Comment(models.Model):
    
    
    name = models.CharField(max_length =50) 
    email = models.CharField(max_length =50) 
    cm = models.TextField() 
    newsid = models.IntegerField() 
    date = models.CharField(max_length =50) 
    time = models.CharField(max_length =50) 

    def __str__(self):
        return self.set_name 
        
