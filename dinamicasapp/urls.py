# -*- coding: utf-8 -*-

from django.conf.urls import url,patterns
from . import views as MViews 
from django.contrib.auth.decorators import login_required, permission_required


urlpatterns = [
    url(r'^$',(MViews.Index)),
    url(r'^addpromo/$',(MViews.addPromo), name='addpromo'),
    url(r'^savequiz/$',(MViews.saveQuiz), name='savequiz'),
    url(r'^rmpromo/$',(MViews.rmPromo), name='rmpromo'),
    url(r'^rmquiz/$',(MViews.rmQuiz), name='rmquiz'),
    url(r'^addfoto/$',(MViews.addFoto), name='addfoto'),

    url(r'^addfotopalabra/$',(MViews.addFotoPalabra), name='addfotopalabra'),
    url(r'^rmpalabra/$',(MViews.rmPalabra), name='rmpalabra'),   
    url(r'^savepalabra/$',(MViews.savePalabra), name='savepalabra'),

    url(r'^setwinner/$',(MViews.setWinner), name='setwinner'),

    url(r'^addfotomarcador/$',(MViews.addFotoMarcador), name='addfotomarcador'),
    url(r'^savemarcador/$',(MViews.saveMarcador), name='savemarcador'),


    #url(r'^addsbc/$',(MViews.addSb), name='addsbc'),   
    url(r'^addcat/$',(MViews.addCat), name='addcat'),   
    url(r'^addscat/$',(MViews.addSCat), name='addscat'),   
    url(r'^rmcat/$',(MViews.rmCat), name='rmcat'),   

    url(r'^savedin/$',(MViews.saveDin), name='savedin'),
    url(r'^dinamica/(?P<pk>[\w-]+)/$',(MViews.addDinamica), name='dinamica'),

    url(r'^addventaja/$',(MViews.addVentaja), name='addventaja'),
    url(r'^rmventaja/$',(MViews.rmVentaja), name='rmventaja'),

    url(r'^saveswiper/$',(MViews.saveSwiper), name='saveswiper'),
    url(r'^rmswiper/$',(MViews.rmSwiper), name='rmswiper'),
    url(r'^saveimgswiper/$',(MViews.saveImSwiper), name='saveimgswiper'),
    url(r'^rmimgswiper/$',(MViews.rmImSwiper), name='rmimgswiper'),


    url(r'^savedinter/$',(MViews.saveDinTer), name='savedinter'),



]

