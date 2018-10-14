# -*- coding: utf-8 -*-

from django.conf.urls import url,patterns
from . import views as MViews 
from django.contrib.auth.decorators import login_required, permission_required


urlpatterns = [
    url(r'^$',(MViews.Index)),
   url(r'^promos/(?P<kword>[\w-]+)/$',(MViews.Promofilter), name='busqueda'),     
   url(r'^promo/(?P<pk>[\w-]+)/$',(MViews.Detailpromo), name='promo'),     

]

