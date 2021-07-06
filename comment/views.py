from django.shortcuts import render, get_object_or_404, redirect 
from .models import Comment 
from news.models import News 
from cat.models import Cat 
from subcat.models import SubCat
from django.core.files.storage import FileSystemStorage
from trending.models import Trending 
#For login page 
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.models import User
#For manager to manage all the required users in the panel
from manager.models import Manager 
 


def news_cm_add(request,pk):

    return redirect('home')
    