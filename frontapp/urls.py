# -*- coding: utf-8 -*-

from django.conf.urls import url,patterns
from . import views as MViews 
from django.contrib.auth.decorators import login_required, permission_required


urlpatterns = [
    url(r'^$',(MViews.Index)),
    url(r'^calendario/$',MViews.calendarioDin,name='calendario'),
    url(r'^dw/$',MViews.Downloads,name='dw'),
    url(r'^createsopa/$',MViews.createSopa,name='createsopa'),
    url(r'^login/$',MViews.Signin,name='login'),
    url(r'^registro/$',MViews.Register,name='registro'),
    url(r'^allp/$',MViews.allPromos,name='allp'),
    url(r'^exmfront/$',MViews.Exfront,name='exmfront'),
    url(r'^participando/$',MViews.Participa,name='participando'),
    url(r'^resultados/(?P<pks>[\w-]+)/$',MViews.Resultado,name='resultados'),
    url(r'^categorias/$',MViews.indexCategoria,name='categorias'),
    url(r'^promocion/(?P<pks>[\w-]+)/$',(MViews.Detail), name='section'),   
    url(r'^rmparti/(?P<upk>[\w-]+)/(?P<dpk>[\w-]+)/$',(MViews.rmParti), name='rmparti'),   


]

