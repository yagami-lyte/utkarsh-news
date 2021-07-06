from django.shortcuts import render, get_object_or_404, redirect 
from .models import Cat


def cat_list(request):
    
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


    return render(request , 'back/cat_list.html' , {'cat' : cat , 'perm' : perm})



def cat_add(request):
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

    if request.method == 'POST' : 
        name = request.POST.get('name')

        if name == "" :

            error = "All Fields Required"
            return render(request , 'back/error.html' , {'error' : error}) 


        if len(Cat.objects.filter(name = name)) != 0 :
            error = "This Name Used Before"
            return render(request , 'back/error.html' , {'error' : error}) 


        b = Cat(name = name)
        b.save()

        return redirect('cat_list') 



    return render(request , 'back/cat_add.html' , {'perm' : perm})



#Function to delete a category 
def cat_del(request , pk):

    #Login Check Start
    if not request.user.is_authenticated :
        return redirect('my_login')
    #Login Check End 

    b = Cat.objects.filter(pk=pk)
    b.delete()

    return redirect('cat_list')
















