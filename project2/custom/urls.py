from django.urls import path
from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),

    url(r'^logout',views.logout_karo,name='logout_karo'),

    url(r'^god_home',views.god_home,name='god_home'),
    url(r'^god_login',views.god_login,name='god_login'),
    url(r'^god_author',views.god_author,name='god_author'),

    url(r'^sys_home',views.sys_home,name='sys_home'),
    url(r'^sys_login',views.sys_login,name='sys_login'),
    url(r'^sys_author',views.sys_author,name='sys_author'),

    url(r'^update',views.update,name='update'),    
    url(r'^register',views.register,name='register'),    
    url(r'^transfer',views.transfer,name='transfer'),    
    url(r'^deport',views.deport,name='deport'),    
    url(r'^quarantine',views.quarantine,name='quarantine'),    
    url(r'^change_password',views.change_password,name='change_password'),
    url(r'^change_pass_form',views.change_pass_form,name='change_pass_form')


]

urlpatterns+=staticfiles_urlpatterns()
