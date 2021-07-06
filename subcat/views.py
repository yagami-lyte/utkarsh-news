from django.shortcuts import render, get_object_or_404, redirect 
from .models import SubCat
from cat.models import Cat 



def subcat_list(request):

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

    subcat = SubCat.objects.all()


    return render(request , 'back/subcat_list.html' , {'subcat' : subcat , 'perm' : perm})


def subcat_add(request):

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

    cat = Cat.objects.all()

    #Get all the entered data
    if request.method == 'POST' : 
        name = request.POST.get('name')
        catid = request.POST.get('cat')

        #Error Page
        if name == "" :
            error = "All Fields Required"
            return render(request , 'back/error.html' , {'error' : error}) 


        if len(SubCat.objects.filter(name = name)) != 0 :
            error = "This Name Used Before"
            return render(request , 'back/error.html' , {'error' : error}) 

        catname = Cat.objects.get(pk = catid).name 

        #Store it in the database
        b = SubCat(name = name , catname = catname , catid = catid)
        b.save()

        return redirect('subcat_list')
    return render(request , 'back/subcat_add.html' , {'cat' : cat , 'perm' : perm})


#Function to delete subcat from the Panel
def subcat_del(request , pk):

    #Login Check Start
    if not request.user.is_authenticated :
        return redirect('my_login')
    #Login Check End 

    b = SubCat.objects.filter(pk=pk)
    b.delete()

    return redirect('subcat_list')

















