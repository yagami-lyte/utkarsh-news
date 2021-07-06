
from django.conf.urls import url 
from . import views 

urlpatterns = [

    url(r'^newsletter/add/$' , views.news_letter , name = 'news_letter'),
    url(r'^newsletter/emails/$' , views.news_emails, name = 'news_emails'),
    url(r'^newsletter/phones/$' , views.news_phones, name = 'news_phones'),
    url(r'newsletter/del/(?P<pk>\d+)/(?P<num>\d+)/$' , views.news_txt_del , name = 'news_txt_del')

   

]
