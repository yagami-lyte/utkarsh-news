from django.shortcuts import render, get_object_or_404, redirect 
from .models import News 
from main.models import Main 
from django.core.files.storage import FileSystemStorage
import datetime 
from subcat.models import SubCat 
from cat.models import Cat 
from trending.models import Trending


def news_detail(request , word):
    
    #For site settings
    site = Main.objects.get(pk = 2 )

    #For Featured Posts 
    news = News.objects.all().order_by('-pk')
    cat = Cat.objects.all() 
    subcat = SubCat.objects.all()
    lastnews = News.objects.all().order_by('-pk')[:3]
    popnews = News.objects.all().order_by('-pk')[:3]
    trending = Trending.objects.all().order_by('-pk')

    #For news Detail
    shownews = News.objects.filter(name = word)

    mynew = News.objects.filter(name=word)
    mynews = mynew[0] 


    mynews.show = mynews.show +1 
    mynews.save() 

    codes = News.objects.filter(name=word)
    code = codes[0].pk


    return render(request , 'front/news_detail.html' , {'news' : news , 'site' : site,'site' : site , 'shownews' : shownews , 'cat' : cat , 'subcat' : subcat , 'lastnews' : lastnews , 'popnews':popnews , 'trending' : trending , 'code' : code})


def news_list(request):

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

    news = News.objects.all().order_by('-creation_time') 

    return render(request , 'back/news_list.html', {'news' : news , 'perm' : perm})




def news_add(request):
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

    now = datetime.datetime.now()
    year = now.year 
    month = now.month
    day = now.day 

    if len(str(day)) == 1 :
        day = "0" + str(day)
    if len(str(month)) == 1: 
        month = "0" + str(month) 

    today = str(year) + "/" + str(month) + "/"  + str(day)

    hour = now.hour 
    minute = now.minute 

    if len(str(hour)) == 1 :
        hour = "0" + str(hour) 
    if len(str(minute)) == 1 :
        minute = "0" + str(minute)


    time = str(hour) + ":" + str(minute)

    cat = SubCat.objects.all() 


    if request.method == 'POST' :
        
        #Get the entered value on the sreen by request.POST.get syntax 
        newstitle = request.POST.get('newstitle')
        newscat = request.POST.get('newscat')
        newstxtshort = request.POST.get('newstxtshort')
        newstxt = request.POST.get('newstxt')
        newsid = request.POST.get('newscat')

        #Validations--- whether all fields are filled or not
        if newstitle == "" or newstxtshort == "" or newstxt == "" or newscat == "":
            error = "All Fields Required"
            return render(request , 'back/error.html' , {'error' : error}) 
        
        
        try :
            #Upload and save the image
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name , myfile)
            url = fs.url(filename)

            #Check if fileis image format or not
            if str(myfile.content_type).startswith("image"):

                if myfile.size < 5000000 :
                    
                    #Category name
                    newsname = SubCat.objects.get(pk = newsid).name 
                    ocatid = SubCat.objects.get(pk = newsid).catid 
                     
                    #Save to Database
                    b = News(name=newstitle , short_txt = newstxtshort , body_txt = newstxt , date = today ,picname = filename , picurl=url , writer = "-" , catname = newsname , catid = newsid ,show = 0 , time = time , ocatid = ocatid)
                    b.save()

                    count = len(News.objects.filter(ocatid = ocatid))

                    b = Cat.objects.get(pk = ocatid)
                    b.count = count 
                    b.save() 
                    
                    return redirect('news_list')
                
                else:
                    fs = FileSystemStorage()
                    fs.delete(b.picname)

                    
                    error = "Your File Larger Than 5 MB" 
                    return render(request , 'back/error.html' , {'error' : error })

            else:

                #Delete the image since its not supported
                fs = FileSystemStorage()
                fs.delete(b.picname) 

                error = "Your File Not Supported" 
                return render(request , 'back/error.html' , {'error' : error })
            return render(request , 'back/news_add.html' , {'cat' : cat})

 

    

        except : 
            error = "Please input your image" 
            

    return render(request , 'back/news_add.html' , {'cat' : cat , 'perm' : perm})


def news_delete(request,pk):
    #Login Check Start
    if not request.user.is_authenticated :
        return redirect('my_login')
    #Login Check End 

    b = News.objects.get(pk=pk)

    fs = FileSystemStorage()
    fs.delete(b.picname)

    
    ocatid = News.objects.get(pk = pk).ocatid

    b.delete() 
        
    count = len(News.objects.filter(ocatid = ocatid))
    
    m = Cat.objects.get(pk = ocatid)
    m.count = count 
    m.save() 
        
 
    return redirect('news_list')


def news_edit(request,pk):

    #Login Check Start
    if not request.user.is_authenticated :
        return redirect('my_login')
    #Login Check End 



    news = News.objects.get(pk = pk)
    cat = SubCat.objects.all()

    if request.method == 'POST' :
        newstitle = request.POST.get('newstitle')
        newscat = request.POST.get('newscat')
        newstxtshort = request.POST.get('newstxtshort')
        newstxt = request.POST.get('newstxt')
        newsid = request.POST.get('newscat')

        if newstitle == "" or newstxtshort == "" or newstxt == "" or newscat == "":
            error = "All Fields Required"
            return render(request , 'back/error.html' , {'error' : error}) 
        
        
        try :
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name , myfile)
            url = fs.url(filename)

            if str(myfile.content_type).startswith("image"):

                if myfile.size < 5000000 :
                    
                    newsname = SubCat.objects.get(pk = newsid).name 

                    b = News.objects.get(pk = pk)
                    
                    fss = FileSystemStorage()
                    fss.delete(b.picname)

                    b.name = newstitle 
                    b.short_txt = newstxtshort
                    b.body_txt = newstxt
                    b.picname = filename 
                    b.picurl = url
                    b.catname = newsname 
                    b.catid = newsid  
 
                    b.save()
                    return redirect('news_list')
                
                else:
                    
                    error = "Your File Larger Than 5 MB" 
                    return render(request , 'back/error.html' , {'error' : error })

            else:

                fs = FileSystemStorage()
                fs.delete(b.picname) 

                error = "Your File Not Supported" 
                return render(request , 'back/error.html' , {'error' : error })

    

        except : 

            newsname = SubCat.objects.get(pk = newsid).name 

            b = News.objects.get(pk = pk)
                    
            b.name = newstitle 
            b.short_txt = newstxtshort
            b.body_txt = newstxt 
            b.catname = newsname 
            b.catid = newsid  
 
            b.save()
            return redirect('news_list')


 
    return render(request , 'back/news_edit.html' , {'pk' : pk , 'news' : news ,'cat' : cat})


def news_all_show(request,word):
    
    catid = Cat.objects.get(name=word).pk 
    allnews = News.objects.filter(ocatid=catid)


    site = Main.objects.get(pk=2)
    news = News.objects.all().order_by('-pk')
    cat = Cat.objects.all() 
    subcat = SubCat.objects.all()
    lastnews = News.objects.all().order_by('-pk')[:3]
    popnews = News.objects.all().order_by('-show')[:5]
    trending = Trending.objects.all().order_by('-pk')

    lastnews2 = News.objects.all().order_by('-pk')[:4]


    return render(request , 'front/all_news.html' , {'site' : site , 'news' : news , 'cat' : cat , 'subcat' : subcat , 'lastnews' : lastnews , 'popnews' : popnews , 'trending' : trending , 'lastnews2' : lastnews2 , 'allnews' : allnews})


#Publish news after check from admin
def news_publish(request,pk):
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

    news = News.objects.get(pk=pk)
    news.act = 1  
    news.save() 




    return redirect('news_list' , {'perm' : perm})


















