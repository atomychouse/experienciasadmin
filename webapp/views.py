# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import redirect, render, render_to_response
from django.template.context import RequestContext
from django.views.generic import View
from django.contrib.auth.models import User,Group
from djangoules.modelforms import FormCreator
from django import forms
import simplejson
import datetime
from django.contrib.auth import authenticate, login, logout
from django.template.defaultfilters import slugify
import os
from django.conf import settings
import mimetypes
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q
from django.http import JsonResponse
from dinamicasapp.models import * 
import time

class TimeMets():

    def fecha_to_str(self,fecha,formato='%b. %d | %Y'):
        try:
            return datetime.datetime.strftime(fecha,formato)
        except:
            return datetime.datetime.now()
    def fecha_timestamp(self,fecha):
        try:
            return time.mktime(fecha.timetuple())*1000
        except:
            return datetime.datetime.now()





class Index(View,TimeMets):
    template = 'webapp/index.html'            
    def get(self, request,pks=None):
        qs = [] 
        context = {}
        '''
        DESTACADOS
        '''
        hoy = datetime.datetime.now() 
        qs.append( Q(fecha_publicacion__isnull=True) | Q(fecha_publicacion__lte=hoy) & Q(status='publish') & Q(vigencia__gte=hoy))
        host = request.get_host()
        prms = Promocion.objects.filter(status='publish',vigencia__gte=hoy).order_by('-destacado','orden','-vigencia',)
        prms = Promocion.objects.all()
        cats = Promocat.objects.filter(parentcat__isnull=False)
        promos_destacados = [ 
                    {   
                    "vigencia":self.fecha_to_str(p.vigencia), 
                    'ciudad':p.ciudad,
                    'destacado':p.destacado,
                    'lugar':p.lugar, 
                    'imagen':'http://%s%s'%(host,p.img), 
                    "titulo": p.linea_uno,
                    "titulo_color": p.linea_dos,
                    "titulo_completo":'%s %s'%(p.linea_uno,p.linea_dos), 
                    "participaciones": p.participacion_set.all().count(), 
                    "likes": p.delikes_set.all().count(),
                    "orden":p.orden, 
                    "dinamica":p.dinamica,
                    "categorias":p.categorias,
                    "segmentos":p.segmentos, 
                    "pk": p.pk, 
                    }
                     for p in prms]
        context['destacados'] = promos_destacados[0:3]
        context['todos'] = promos_destacados[3:]
        context['cats'] = cats
        response = render(request, self.template, context)
        return response

Index = Index.as_view()


class Promofilter(View,TimeMets):
    template = 'webapp/search.html'            
    def get(self, request,kword=None):            
        qs = [] 
        context = {}
        '''
        DESTACADOS
        '''
        hoy = datetime.datetime.now() 
        qs.append( Q(fecha_publicacion__isnull=True) | Q(fecha_publicacion__lte=hoy) & Q(status='publish') & Q(vigencia__gte=hoy))
        host = request.get_host()
        
        if kword:
            qs.append(Q(categorias__icontains=kword))

        prms = Promocion.objects.filter(*qs).order_by('-destacado','orden','-vigencia')
        cats = Promocat.objects.filter(parentcat__isnull=False)
        promos_destacados = [ 
                    {   
                    "vigencia":self.fecha_to_str(p.vigencia), 
                    "fecha_evento":self.fecha_to_str(p.fecha_evento),
                    "fecha_publicacion":self.fecha_to_str(p.fecha_publicacion),
                    "dia_evento":self.fecha_to_str(p.fecha_evento,formato='%d'),
                    "mes_evento":self.fecha_to_str(p.fecha_evento,formato='%b'),
                    'ciudad':p.ciudad,
                    'destacado':p.destacado,
                    'lugar':p.lugar, 
                    "vigenciaUTC": time.mktime(p.vigencia.timetuple()),
                    'imagen':'http://%s%s'%(host,p.img), 
                    "titulo": p.linea_uno,
                    "titulo_color": p.linea_dos,
                    "titulo_completo":'%s %s'%(p.linea_uno,p.linea_dos), 
                    "participaciones": p.participacion_set.all().count(), 
                    "likes": p.delikes_set.all().count(),
                    "orden":p.orden, 
                    "dinamica":p.dinamica,
                    "categorias":p.categorias,
                    "segmentos":p.segmentos, 
                    "pk": p.pk, 
                    }
                     for p in prms]

        context['catsearch'] = cats.filter(catslug=kword)

        context['destacados'] = promos_destacados
        context['cats'] = cats
        response = render(request, self.template, context)
        return response
        
Promofilter = Promofilter.as_view()



class Detailpromo(View,TimeMets):
    template = 'webapp/detail.html'            
    def get(self, request,pk=None):            
        host = request.get_host()
        qs = [] 
        context = {}
        p = Promocion.objects.get(pk=pk)
        context['fullp'] = p
        promos_destacados = {   
                    "vigencia":self.fecha_to_str(p.vigencia), 
                    "fecha_evento":self.fecha_to_str(p.fecha_evento),
                    "fecha_publicacion":self.fecha_to_str(p.fecha_publicacion),
                    "dia_evento":self.fecha_to_str(p.fecha_evento,formato='%d'),
                    "mes_evento":self.fecha_to_str(p.fecha_evento,formato='%b'),
                    'ciudad':p.ciudad,
                    'destacado':p.destacado,
                    'lugar':p.lugar, 
                    "vigenciaUTC": time.mktime(p.vigencia.timetuple()),
                    'imagen':'http://%s%s'%(host,p.imglg), 
                    "titulo": p.linea_uno,
                    "titulo_color": p.linea_dos,
                    "titulo_completo":'%s %s'%(p.linea_uno,p.linea_dos), 
                    "participaciones": p.participacion_set.all().count(), 
                    "likes": p.delikes_set.all().count(),
                    "orden":p.orden, 
                    "dinamica":p.dinamica,
                    "categorias":p.categorias,
                    "segmentos":p.segmentos, 
                    "pk": p.pk, 
                    'premio':p.premio
                    }
         
        context['promos'] = [ 
                    {   
                    "vigencia":self.fecha_to_str(p.vigencia), 
                    "fecha_evento":self.fecha_to_str(p.fecha_evento),
                    "fecha_publicacion":self.fecha_to_str(p.fecha_publicacion),
                    "dia_evento":self.fecha_to_str(p.fecha_evento,formato='%d'),
                    "mes_evento":self.fecha_to_str(p.fecha_evento,formato='%b'),
                    'ciudad':p.ciudad,
                    'destacado':p.destacado,
                    'lugar':p.lugar, 
                    "vigenciaUTC": time.mktime(p.vigencia.timetuple()),
                    'imagen':'http://%s%s'%(host,p.img), 
                    "titulo": p.linea_uno,
                    "titulo_color": p.linea_dos,
                    "titulo_completo":'%s %s'%(p.linea_uno,p.linea_dos), 
                    "participaciones": p.participacion_set.all().count(), 
                    "likes": p.delikes_set.all().count(),
                    "orden":p.orden, 
                    "dinamica":p.dinamica,
                    "categorias":p.categorias,
                    "segmentos":p.segmentos, 
                    "pk": p.pk, 
                    }
                     for p in Promocion.objects.all()]

        context['p'] = promos_destacados

        response = render(request, self.template, context)
        return response
        
Detailpromo = Detailpromo.as_view()

