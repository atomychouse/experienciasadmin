# -*- coding: utf-8 -*-

from django.conf.urls import url,patterns
from . import views as MViews 
from django.contrib.auth.decorators import login_required, permission_required


urlpatterns = [
    url(r'^$',login_required(MViews.Index)),
    url(r'^calendario/$',login_required(MViews.calendarioDin),name='calendario'),
    url(r'^dw/$',login_required(MViews.Downloads),name='dw'),
    url(r'^createsopa/$',login_required(MViews.createSopa),name='createsopa'),
    url(r'^login/$',(MViews.Signin),name='login'),
    url(r'^sin/$',(MViews.Sin),name='sin'),
    url(r'^registro/$',login_required(MViews.Register),name='registro'),
    url(r'^allp/$',login_required(MViews.allPromos),name='allp'),
    url(r'^exmfront/$',login_required(MViews.Exfront),name='exmfront'),
    url(r'^participando/$',login_required(MViews.Participa),name='participando'),
    url(r'^resultados/(?P<pks>[\w-]+)/$',login_required(MViews.Resultado),name='resultados'),
    url(r'^categorias/$',login_required(MViews.indexCategoria),name='categorias'),
    url(r'^promocion/(?P<pks>[\w-]+)/$',login_required(MViews.Detail), name='section'),   
    url(r'^rmparti/(?P<upk>[\w-]+)/(?P<dpk>[\w-]+)/$',login_required(MViews.rmParti), name='rmparti'),   


    url(r'^addferiado/$',login_required(MViews.addFeriado),name='addferiado'),
    url(r'^rmferiado/$',login_required(MViews.rmFeriado),name='rmferiado'),



]

