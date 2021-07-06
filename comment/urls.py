from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^comment/comment/add/(?P<pk>\d+)/$' , views.news_cm_add , name = 'news_cm_add'),



] 