from __future__ import unicode_literals
from django.db import models


class Cat(models.Model):
    name = models.CharField(max_length = 50)
    count = models.IntegerField(default = 0)
     
    

    def __str__(self):
        return self.name 

