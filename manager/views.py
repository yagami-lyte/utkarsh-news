from django.shortcuts import render, get_object_or_404, redirect, resolve_url 
from .models import Manager
from news.models import News 
from cat.models import Cat 
from subcat.models import SubCat
from django.core.files.storage import FileSystemStorage
from trending.models import Trending 
#For login page 
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.models import User
from django.contrib.auth.models import User,Group,Permission

#Display all the users list 
def manager_list(request):

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

    manager = Manager.objects.all()

    return render(request , 'back/manager_list.html' , {'manager':manager , 'perm' : perm})


#Delete a user account 
def manager_del(request , pk):

    
    manager = Manager.objects.get(pk=pk)
    b = User.objects.filter(username = manager.utxt)
    b.delete()

    manager.delete()


    return redirect('manager_list') 



############# MAKE GROUPS TO BIFERCATE USERS AND ADMIN #########
 
#List out all the groups made
def manager_group(request):

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

    group = Group.objects.all().order_by('-pk')

    return render(request , 'back/manager_group.html' , {'group' : group , 'perm' : perm})


#Add the groups from the panel
def manager_group_add(request):

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

        if name != "" :

            #If group is empty, publish it! 
            
            group = Group(name=name)
            group.save()  

    return redirect('manager_group')

#Delete a Groupsss
def manager_group_del(request , name):

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

    #Delete
    b = Group.objects.filter(name=name)
    b.delete()  

    return redirect('manager_group')

#Add groups to the users or add users to the groups
def users_groups(request,pk):

    #Get the users username based on pk
    manager = Manager.objects.get(pk=pk)
    user = User.objects.get(username=manager.utxt)
    
    #Add all the user's groups  
    ugroup = [] 
    for i in user.groups.all():
        ugroup.append(i.name)

    group = Group.objects.all() 

    return render(request , 'back/users_group.html' , {'ugroup' : ugroup , 'group' : group , 'pk':pk})

#One pk for groups and another name for which user is being added 
#will be passed in the function
def add_users_to_groups(request,pk): 

    if request.method == 'POST' :

        gname = request.POST.get('gname')
        
        group = Group.objects.get(name=gname)
        manager = Manager.objects.get(pk=pk)
        user = User.objects.get(username=manager.utxt)

        #Add the group to the user
        user.groups.add(group)


    #Pass on the pk value for further acceptance
    return redirect('users_groups' , pk=pk)

#Delete the gorups addigned to the users
def del_users_to_groups(request,pk,name): 

    group = Group.objects.get(name= name)
    manager = Manager.objects.get(pk=pk)
    user = User.objects.get(username=manager.utxt)
    user.groups.remove(group)


    #Pass on the pk value for further acceptance
    return redirect('users_groups' , pk=pk)




