from __future__ import unicode_literals 
from django.db import models 

class Main(models.Model):
    
    about = models.TextField()
    abouttxt = models.TextField(default="")
    
    name = models.CharField(max_length =20) 
    fb = models.CharField(default = "-" , max_length = 20)
    tw = models.CharField(default = "-", max_length = 20)
    yt = models.CharField(default = "-", max_length = 20)
    set_name = models.CharField(default = "-" , max_length = 20)
    
    tel= models.CharField(default = "-", max_length = 20)
    link = models.CharField(default = "-", max_length = 20)

    picurl = models.TextField(default = "")
    picname = models.TextField(default = "")


    def __str__(self):
        return self.set_name + " " + str(self.pk)
        
