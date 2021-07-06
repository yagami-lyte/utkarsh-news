from django.shortcuts import render, get_object_or_404, redirect 
from .models import Main 
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

from django.contrib.auth.models import User,Group,Permission

from django.contrib.auth.models import User 

def home(request):
    site = Main.objects.get(pk=2)
    
    #Act=1 indicates whether the news will be puclished or not
    #Add this in all news queries
    news = News.objects.filter(act=1).order_by('-pk')
    cat = Cat.objects.all() 
    subcat = SubCat.objects.all()
    #REcent Posts News
    lastnews = News.objects.filter(pk=1).order_by('-pk')[:3]

    #News Details Side bar Popular posts
    popnews = News.objects.filter(act=1).order_by('-show')[:5]
    trending = Trending.objects.all().order_by('-pk')

    lastnews2 = News.objects.filter(act=1).order_by('-pk')[:4]


    return render(request , 'front/home.html' , {'site' : site , 'news' : news , 'cat' : cat , 'subcat' : subcat , 'lastnews' : lastnews , 'popnews' : popnews , 'trending' : trending , 'lastnews2' : lastnews2})

def about(request):
    site = Main.objects.get(pk=2)
    news = News.objects.all().order_by('-pk')
    cat = Cat.objects.all() 
    subcat = SubCat.objects.all()
    lastnews = News.objects.all().order_by('-pk')[:3]
    popnews = News.objects.all().order_by('-show')[:3]
    trending = Trending.objects.all().order_by('-pk')

    site = Main.objects.get(pk=2)
    return render(request , 'front/about.html' , {'site' : site , 'news' : news , 'cat' : cat , 'subcat' : subcat , 'lastnews' : lastnews , 'popnews' : popnews ,'trending' : trending})


def panel(request):

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
    
    return render(request , 'back/home.html' , {'perm' : perm})



#A login page view function 
def my_login(request): 

    #The data can be sent from the form to the views function
    #same as upass and user are connected to the form action in login.html
    if request.method == 'POST':

        utxt = request.POST.get('username')
        ptxt = request.POST.get('password')

        if utxt != "" and ptxt != "" :

            user = authenticate(username=utxt , password = ptxt)

            if user != None :
                login(request , user)
                return redirect('panel')


    
    return render(request , 'front/login.html')


#For registering an acount on login.html
def my_register(request): 

    if request.method == 'POST':
        name = request.POST.get('name')
        uname = request.POST.get('uname')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if name == "" :
            msg = "Input Your Name"
            return render(request , 'front/msgbox.html' , {'msg' : msg})

            
        if password1 != password2 :
            msg = "Your Password Did not match"
            return render(request , 'front/msgbox.html', {'msg' : msg})

        #Check whether password is Strong enough
        #Start
        count1 = 0 
        count2 = 0 
        count3 = 0 
        count4 = 0 

        for i in password1:
            if i>"0" and i<"9" :
                count1 = 1 
            if i>"A" and i<"Z" :
                count2 = 1 
            if i>"a" and i<"z":
                count3 = 1
            if i>"!" and i<"" :
                count4 = 1 

        if count1 == 0 or count2 == 0 or count3 == 0 or count4 == 4 :
            msg = "Your Password is not Strong"
            return render(request , 'front/msgbox.html', {'msg' : msg})
        
        if len(password1) < 8 :
            msg = "Your Password must be 8 characters"
            return render(request , 'front/msgbox.html', {'msg' : msg})
        #END

        
        if len(User.objects.filter(username=uname)) == 0 and len(User.objects.filter(email=email)) == 0 :
            user = User.objects.create_user(username=uname , email = email , password = password1)
            b = Manager(name=name , utxt = uname , email=email)
            b.save()





    
    return render(request , 'front/login.html')    

#Logout Function 
def my_logout(request):

    logout(request)

    return  redirect('my_login')
    

def site_setting(request):

    #Login check Start
    if not request.user.is_authenticated :
        return redirect( 'mlogin' )
    #Login check end 

    #If user is master user or admin then hes allowed to access this section
    #Users who doesnt belong to this group are not authorised to this section
    #CHECK START
    perm = 0 
    for i in request.user.groups.all(): 
        if i.name == "masteruser" : perm = 1 

    if perm == 0 :
        error = "Access Denied"
        return render(request , 'back/error.html' , {'error' : error}) 
    #CHECK END    

    

    if request.method == 'POST' : 
        name = request.POST.get('name')
        tel = request.POST.get('tel')
        fb = request.POST.get('fb')
        tw = request.POST.get('tw')
        yt = request.POST.get('yt')
        link = request.POST.get('link')
        txt = request.POST.get('txt')

        if fb == "" : fb = "#"
        if tw == "" : tw = "#"
        if yt == "" : yr = "#"



        if name == "" or tel == "" or txt == "" :
            error = "All Fields Required"
            return render(request , 'back/error.html' , {'error' : error})


        try : 
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name , myfile)
            url = fs.url(filename)

            b = Main.objects.get(pk=2)
            b.name = name
            b.tel = tel
            b.fb = fb 
            b.tw = tw 
            g.yt = yt 
            b.link = link 
            b.about = txt 
            b.picurl = url 
            b.picname = filename
            b.save()


        except:

            b = Main.objects.get(pk=2)
            b.name = name
            b.tel = tel
            b.fb = fb 
            b.tw = tw 
            b  .yt = yt 
            b.link = link 
            b.about = txt 
            b.save()
            
    site = Main.objects.get(pk = 2)

    return render(request , 'back/setting.html' , {'site' : site , 'perm' : perm})


def about_setting(request):

    #Login check Start
    if not request.user.is_authenticated :
        return redirect( 'mlogin' )
    #Login check end 

    #If user is master user or admin then hes allowed to access this section
    #Users who doesnt belong to this group are not authorised to this section
    #CHECK START
    perm = 0 
    for i in request.user.groups.all(): 
        if i.name == "masteruser" : perm = 1 

    if perm == 0 :
        error = "Access Denied"
        return render(request , 'back/error.html' , {'error' : error}) 
    #CHECK END    

    if request.method == 'POST' :
        txt = request.POST.get('txt')

        if txt == "" :
            error = "All Fields Required"
            return render(request , 'back/error.html' , {'error' : error})
        
        b = Main.objects.get(pk=2)
        b.abouttxt = txt 
        b.save()

 

    about = Main.objects.get(pk=2).abouttxt

    return render(request , 'back/about_setting.html' , {'about' : about , 'perm' : perm})

def contact(request):
    site = Main.objects.get(pk=2)
    news = News.objects.all().order_by('-pk')
    cat = Cat.objects.all() 
    subcat = SubCat.objects.all()
    lastnews = News.objects.all().order_by('-pk')[:3]
    popnews = News.objects.all().order_by('-show')[:3]
    trending = Trending.objects.all().order_by('-pk')


    return render(request , 'front/contact.html' , {'site' : site , 'news' : news , 'cat' : cat , 'subcat' : subcat , 'lastnews' : lastnews , 'popnews' : popnews , 'trending' : trending})

def change_pass(request):
    #Login check Start
    if not request.user.is_authenticated :
        return redirect( 'mlogin' )
    #Login check end 

    if request.method == 'POST' : 
        oldpass = request.POST.get('oldpass')
        newpass = request.POST.get('newpass')

        if oldpass == "" or newpass == "" : 
            error = "All Fields Required"
            return render(request , 'back/error.html' , {'error' : error})

        user = authenticate(username = request.user , password = oldpass)

        if user != None :
            if len(newpass) < 8 : 
                error = "Your Password Must be atleast 8 characters"
                return render(request , 'back/error.html' , {'error' : error})
  
        count1 = 0  
        count2 = 0  
        count3 = 0  
        count4 = 0 

        for i in newpass : 
            if i > "0" and i < "9" : 
                count1 = 1 
            if i > "A" and i < "Z" : 
                count2 = 1 
            if i > "a" and i < "z" :
                count3 = 1 

        if count1 == 1 and count2  == 1 and count3 == 1: 
            user = User.objects.get(username = request.user)
            user.set_password(newpass)
            user.save()  
            return redirect('my_logout')

        else :
            error = "Password is not Strong Enough"
            return render(request , 'back/error.html' , {'error' : error})
        


        
        

    return render(request , 'front/change_pass.html')