# -*- coding: utf-8 -*-

from django.conf.urls import url,patterns
from . import views as MViews 
from django.contrib.auth.decorators import login_required, permission_required


urlpatterns = [
   url(r'^$',(MViews.Index), name='inicio'),
   url(r'^addfont/$',(MViews.addFont), name='addfont'),
   url(r'^addcolor/$',(MViews.addColor), name='addcolor'),
    url(r'^addsett/$',(MViews.addSett), name='addsett'),

]

