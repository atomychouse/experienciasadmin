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
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail, BadHeaderError
from djangoules.settings import *
from django.views.decorators.csrf import csrf_exempt
import time
import os
from django.conf import settings
import mimetypes
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q
from django.http import JsonResponse
from django.utils.html import escape
from django.core.mail import send_mail, EmailMessage
from django.core.mail import send_mass_mail
from django.core.mail import get_connection, EmailMultiAlternatives
from django.template.loader import render_to_string, get_template
from random import randint
from cfgapp.models import *
from django.core.files.base import ContentFile
from base64 import b64decode
import StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile

 

class Index(View):

    template = 'cfgapp/index.html'

    def get(self, request):
        data = request.GET.copy()
        context = {}
        userp = {'name':'Alberto','profile':'admin'}
        t = Tipografia.objects.all()
        c = Color.objects.all()
        colors = [
            {
            'typo':x.tipo,
            'hex':x.color,
            'rgb':x.rgbcolor
            }

            for x in c
        ]
        fonts = [
            {
            'usage':x.uso,
            'puntaje':x.puntaje,
            'namefont':x.namefont()
            }

            for x in t
        ]
        context['user'] = userp
        context['fonts'] = simplejson.dumps(fonts)
        context['colors'] = simplejson.dumps(colors)

        response = render(request, self.template, context)
        return response

Index = Index.as_view()



class addFont(View):

    template = 'cfgapp/index.html'

    def post(self, request):
        context = {}
        data = request.POST.copy()
        strfile = data.get('archivestr',None)
        filename = data.get('filename',None)
        usage = data.get('usage',None)
        puntaje = data.get('puntaje',None)
        current_site = get_current_site(request)
        basepath = settings.BASE_DIR

        if strfile:
            formats, imgstr = strfile.split(';base64,')
            filesafe = ContentFile(b64decode(imgstr),name=filename)

            try:
                t = Tipografia.objects.get(sitio=current_site,uso=usage)
                t.delete()
                os.remove(t.tipofile.path)

            except:
                 t = Tipografia()

        else:
            try:
                t = Tipografia.objects.get(sitio=current_site,uso=usage)
            except:
                t = Tipografia()

        t.sitio = current_site
        t.uso = usage
        t.puntaje = puntaje
        
        if strfile:
            t.tipofile = filesafe
        
        t.save()

        response = {'fontpk':t.pk}
        return JsonResponse(response)
addFont = addFont.as_view()


class addColor(View):
    
    def get(self,request):
        current_site = get_current_site(request)
        data = request.GET.getlist('cual')
        
        for d in data:
            dato = simplejson.loads(d)
            color = dato['colorset']['hex']
            tipo = dato['typo']
            r = dato['colorset']['rgb']['r']
            g = dato['colorset']['rgb']['g']
            b = dato['colorset']['rgb']['b']

            rgbcolor = '%s,%s,%s'%(r,g,b)
            c,b = Color.objects.get_or_create(sitio=current_site,tipo=tipo)
            c.color = color
            c.rgbcolor = rgbcolor
            c.save()

        response = {'cpk':c.pk}
        
        return JsonResponse(response)

addColor = addColor.as_view()


class addSett(View):
    
    def get(self,request):
        current_site = get_current_site(request)
        data = request.GET.copy()
        backcolor = data.get('backcolor',None)
        fontcolor = data.get('fontcolor',None)
        tiposet = 'colorsetts'
        valueset = [backcolor,fontcolor]
        values = simplejson.dumps(valueset)

        st,novalue = Sitesetting.objects.get_or_create(sitio=current_site,tiposet=tiposet)
        st.valueset = values
        st.save()

        response = {'cpk':st.pk}
        
        return JsonResponse(response)

addSett = addSett.as_view()