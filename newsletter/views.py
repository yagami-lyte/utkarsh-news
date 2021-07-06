from django.shortcuts import render, get_object_or_404, redirect 
from .models import Newsletter
from news.models import News 
from cat.models import Cat 
from subcat.models import SubCat
from django.core.files.storage import FileSystemStorage
from trending.models import Trending 
#For login page 
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.models import User



#Create a Function for newslletter
#which saves the news using forms in master.html
def news_letter(request):

    if request.method == 'POST' :
        txt = request.POST.get('txt')

        #check if @ sign is present or not
        res = txt.find('@')
        
        #if yes then save it in the newsletter
        if int(res) != -1 : 
            b = Newsletter(txt=txt , status = 1 )
            b.save()
        #otherwise check for errors
        else:
            #if no error, save it with status 2 
            try : 
                int(txt) 
                b = Newsletter(txt=txt , status = 2)
                b.save()  
            #else redirect to the home page
            except :
                return redirect('home') 



        msg = "Your Email Received"
        return render(request , 'front/msgbox.html' , {'msg' : msg})
         

    return redirect('home')


def news_emails(request):
     #Login Check Start
    if not request.user.is_authenticated :
        return redirect('my_login')
    #Login Check End 

    #If user is master user or admin then hes allowed to access this section
    #Users who doesnt belong to this group are not authorised to this section
    #CHECK START
    perm = 0 
    for i in request.user.groups.all(): 
        if i.name == "masteruser" : perm = 1 

    #CHECK END   


    emails = Newsletter.objects.filter(status = 1)

    return render(request , 'back/emails.html' , {'emails' : emails ,  'perm' : perm})

def news_phones(request):
     #Login Check Start
    if not request.user.is_authenticated :
        return redirect('my_login')
    #Login Check End 

    #If user is master user or admin then hes allowed to access this section
    #Users who doesnt belong to this group are not authorised to this section
    #CHECK START
    perm = 0 
    for i in request.user.groups.all(): 
        if i.name == "masteruser" : perm = 1 

    #CHECK END   


    phones = Newsletter.objects.filter(status = 2)

    return render(request , 'back/phones.html' , {'phones' : phones , 'perm' : perm})


def news_txt_del(request , pk , num):
    #Login Check Start
    if not request.user.is_authenticated :
        return redirect('my_login')
    #Login Check End 

    b = Newsletter.objects.get(pk=pk)
    b.delete() 

    if int(num) == 2 : 
        return redirect('news_phones')

    return redirect('news_emails')
    

