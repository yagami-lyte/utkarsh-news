from django.shortcuts import render, get_object_or_404, redirect 
from .models import Trending 
from news.models import News 
from cat.models import Cat 
from subcat.models import SubCat
from django.core.files.storage import FileSystemStorage


def trending_add(request):

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

    #CHECK END   

    if request.method == 'POST' :
        txt = request.POST.get('txt')

        if txt == "" :
            error = "All Fiedlds Required"
            return render(request , 'back/error/html' , {'error' : error})

        b = Trending(txt = txt)
        b.save() 

    trendinglist = Trending.objects.all()

    return render(request , 'back/trending.html', {'trendinglist' : trendinglist , 'perm' : perm})

#Delete Trending 
def trending_del(request , pk):

    b = Trending.objects.filter(pk=pk)
    b.delete()

    return redirect('trending_add') 


def trending_edit(request , pk):
    mytxt = Trending.objects.get(pk=pk)
    
    if request.method == 'POST' :
        
        txt = request.POST.get('txt')
        
        if txt == "" :
            error = "All Fields Required"
            return render(request , 'back/error.html' , {'error' : error})

        b = Trending.objects.get(pk=pk)
        b.txt = txt
        b.save()

        return redirect('trending_add')



    return render(request , 'back/trending_edit.html' , {'mytxt' : mytxt , 'pk':pk})
