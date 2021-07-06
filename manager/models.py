from __future__ import unicode_literals 
from django.db import models 

class Manager(models.Model):
    
    name = models.CharField(max_length =20) 
    utxt = models.TextField()
    email = models.TextField(default="-")
    


    def __str__(self):
        return self.set_name
        
 