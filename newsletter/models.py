from __future__ import unicode_literals
from django.db import models 

class Newsletter(models.Model):

    txt = models.CharField(max_length=50)
    status = models.IntegerField(default=0)
    

    def __str__(self):
        return self. txt 