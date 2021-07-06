from django.shortcuts import render, get_object_or_404, redirect 
from .models import ContactForm 
from news.models import News 
from cat.models import Cat 
from subcat.models import SubCat
from django.core.files.storage import FileSystemStorage


#Add the contact views here 
def contact_add(request):

    if request.method == 'POST':

        name = request.POST.get('name')
        email = request.POST.get('email')
        txt = request.POST.get('msg')

        if name == "" or email == "" or txt == "" :
            msg = "All Fields Required"
            return render(request , 'front/msgbox.html' , {'msg' : msg})

        b = ContactForm(name=name, email = email , txt = txt )
        b.save()

        msg = "Your Message Received"
        return render(request , 'front/msgbox.html' , {'msg' : msg})
          



    return render(request , 'front/msgbox.html')


#This function governs the panel contact form
#It shows a list of message list which the users 
#enter from the website

def contact_show(request):
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

    msg = ContactForm.objects.all()


    return render(request , 'back/contact_form.html' , {'msg' : msg , 'perm' : perm})


def contact_del(request , pk):

    b = ContactForm.objects.filter(pk=pk)
    b.delete()

    return redirect('contact_show')