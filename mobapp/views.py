# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.http import JsonResponse
#from django.shortcuts import redirect, render, render_to_response
from django.template.context import RequestContext
from django.views.generic import View
from django import forms
import simplejson
import datetime
#from django.contrib.auth import authenticate, login, logout
#from django.contrib.auth.hashers import make_password
#from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
#from django.core.mail import send_mail
from django.template.defaultfilters import slugify
#SISTEM && SETTINGS LIBS
import time
import os
from django.conf import settings
import mimetypes
from django.contrib.sites.shortcuts import get_current_site

#from django.core.mail import EmailMultiAlternatives

#MODELS LIBS
from django.contrib.auth.models import User,Group
from django.db.models import Q
from motorapp.models import * 
from dinamicasapp.models import * 
#IMAGE LIBS
from PIL import Image,ExifTags
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.files import File

from base64 import b64decode
import StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile

import datetime
import pytz
import StringIO

class TimeMets():


    def fecha_to_str(self,fecha,formato='%b. %d | %Y'):
        try:
            return datetime.datetime.strftime(fecha,formato)
        except:
            return None
    def fecha_timestamp(self,fecha):
        try:
            return time.mktime(fecha.timetuple())
        except:
            return None

    def fecha_timestamp_delay(self,fecha):
        fecha += datetime.timedelta(days=1)
        try:
            return time.mktime(fecha.timetuple()) 
        except:
            return None


    def fecha_mktime(self,fecha):
        try:
            return time.mktime(fecha.timetuple())
        except:
            return None

    def strfecha(self,fecha=None):
        try: 
            fechastr = datetime.datetime.strptime(fecha, '%b. %d | %Y')
        except:
            fechastr = None            
        return fechastr


    def segments(self,slug=None):
        segmentos = {
        'clarovideo':'Claro video',
        'claromusica':u'Claro música',
        'clarojuegos':'Claro juegos',
        'clarodrive':'Claro drive',
        'clubclaroapp':'Club Claro apps',
        'claroentretenimiento':'Claro entretenimiento',
        'contestone':'Contestone',
        'apptelcel':'App Telcel'
        }
    

        if slug:
            retorno =  segmentos[slug]
        else:
            retorno =  None


        return retorno


class promoList(View,TimeMets):

    def get(self,request):
        

        data = request.GET.copy()
        recomendados = data.get('recomendados',None)        
        search = {}

        word_sr = data.get('search',None)
        destacados = data.get('destacados',None)
        upk = data.get('upk',None)

        if upk=='no user':
            upk = None

        qs = [] 
        if word_sr:
            qs = [Q(linea_uno__icontains=word_sr) | Q(linea_dos__icontains=word_sr) | Q(linea_tres__icontains=word_sr)]
        if destacados:
            dests = {'true':True,'false':False}
            qs.append(Q(destacado=dests[destacados.lower()]))

        mxtz = pytz.timezone('America/Mexico_City')

        hoy = datetime.datetime.now(mxtz) #+ datetime.timedelta(hours=22)


        '''
        Updating promolist for status=proximamente to pulish 

        '''

        promoupdate = Promocion.objects.filter(status='proximamente',vigencia__gte=hoy,fecha_publicacion=hoy)
        promoupdate.update(status='publish')

        #qs.append( Q(fecha_publicacion__isnull=True) | Q(fecha_publicacion__lte=hoy) )
        host = request.get_host()

        prox = Q(status='proximamente')
        publ = Q(status='publish') & Q(vigencia__gte=hoy)

        todos = Promocion.objects.filter(Q(prox | (publ))).order_by('-destacado','fecha_evento','vigencia')
        #assert False,(qs)
        prms = todos.filter(*qs)

        subtotales = prms.count()

        if destacados and subtotales>0:
            if destacados.lower()=='true':
                if subtotales<4:
                    faltantes = 4 - subtotales
                    extras = todos[0:faltantes]

                    prms = todos[0:4]
                else:
                    prms = prms[0:4]


        if recomendados:
            parts = Participacion.objects.filter(usuario_id=upk,final__isnull=False)
            nopks = [x.promopk_id for x in parts]
            dpk = data.get('dpk',None)
            if dpk:
                nopks.append(dpk)
            prms = Promocion.objects.filter(vigencia__gte=hoy,status='publish').exclude(pk__in=nopks)


        promos = [ 
                    {  
                    'liked':p.yo_like(upk), 
                    "vigencia":self.fecha_to_str(p.vigencia), 
                    "fecha_evento":self.fecha_to_str(p.fecha_evento),
                    "fecha_publicacion":self.fecha_to_str(p.fecha_publicacion),
                    "dia_evento":self.fecha_to_str(p.fecha_evento,formato='%d'),
                    "mes_evento":self.fecha_to_str(p.fecha_evento,formato='%b'),
                    'ciudad':p.ciudad,
                    'status':p.status,
                    'destacado':p.destacado,
                    'lugar':p.lugar, 
                    "vigenciaUTC": time.mktime(p.vigencia.timetuple()),
                    'imagen':'https://%s%s'%(host,p.img), 
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
                    'participo':p.yaparticipo(upk)
                    }
                     for p in prms]

        hoy = datetime.datetime.now(mxtz)
        ventaja = Pagesetts.objects.filter(fin__gte=hoy).order_by('fin').first()
        if ventaja:
            vtext = self.segments(ventaja.ventaja)
            ven = ventaja.ventaja
            texto = '%s al %s de %s'%(self.fecha_to_str(ventaja.inicio,formato='%d'),self.fecha_to_str(ventaja.fin,formato='%d'),self.fecha_to_str(ventaja.fin,formato='%B'))
            terminosventaja = ventaja.terminos
            
        else:
            ven = ''
            vtext = ''
            texto = ''
            terminosventaja = ''

        promos = {'dinamicas':promos,'totales':len(promos),'ventaja':ven,'ventaja_texto':vtext,'fecha_ventaja':texto,'ventajaterminos':terminosventaja}
        return JsonResponse(promos)

promoList = promoList.as_view()



class promoEnd(View,TimeMets):

    def get(self,request):

        mxtz = pytz.timezone('America/Mexico_City')       
        data = request.GET.copy()
        hoy = datetime.datetime.now(mxtz) 
        host = request.get_host()


        prms = Promocion.objects.filter(status__in=['finalizado']).order_by('-vigencia')
        #prms = prms.filter(*qs)

        sinfinalizar = [] #Promocion.objects.filter(vigencia__lte=hoy,status__in=['publish']).order_by('fecha_evento','vigencia')
        promos = [ 
                    {   
                    "vigencia":self.fecha_to_str(p.vigencia), 
                    "fecha_evento":self.fecha_to_str(p.fecha_evento),
                    "fecha_publicacion":self.fecha_to_str(p.fecha_publicacion),
                    "dia_evento":self.fecha_to_str(p.fecha_evento,formato='%d'),
                    "mes_evento":self.fecha_to_str(p.fecha_evento,formato='%b'),
                    'ciudad':p.ciudad,
                    'status':'finalizado',
                    'lugar':p.lugar, 
                    "vigenciaUTC": time.mktime(p.vigencia.timetuple()),
                    'imagen':p.finalimg_min(host),
                    'imagen_ganadores':p.finalimg(host), 
                    #"titulo": p.linea_uno,
                    #"titulo_color": p.linea_dos,
                    #"titulo_completo":'%s %s'%(p.linea_uno,p.linea_dos), 
                    'titulo_final':p.header_final,
                    'texto_final':p.texto_alterno,
                    "shares": p.shares, 
                    "likes":p.delikes_set.all().count(),
                    "ganadores_total":p.participacion_set.filter(ganadora=True).count(),
                    "ganadores_list":[
                        {'nombre':g.usuario.username,
                        'img':g.imagenuser()}
                         for g in p.participacion_set.filter(ganadora=True)],
                    "orden":p.orden, 
                    "dinamica":p.dinamica,
                    "categorias":p.categorias,
                    "segmentos":p.segmentos, 
                    "pk": p.pk, 
                    }
                     for p in prms]

        for p in sinfinalizar:
            promomas = {   
            "vigencia":self.fecha_to_str(p.vigencia), 
            "fecha_evento":self.fecha_to_str(p.fecha_evento),
            "fecha_publicacion":self.fecha_to_str(p.fecha_publicacion),
            "dia_evento":self.fecha_to_str(p.fecha_evento,formato='%d'),
            "mes_evento":self.fecha_to_str(p.fecha_evento,formato='%b'),
            'ciudad':p.ciudad,
            'status':'espera',
            'lugar':p.lugar, 
            "vigenciaUTC": time.mktime(p.vigencia.timetuple()),
            'imagen':'https://%s%s'%(host,p.img),
            'imagen_ganadores':'https://%s%s'%(host,p.img), 
            #"titulo": p.linea_uno,
            #"titulo_color": p.linea_dos,
            #"titulo_completo":'%s %s'%(p.linea_uno,p.linea_dos), 
            'titulo_final':p.linea_uno,
            'texto_final':p.linea_dos,
            "shares": p.shares, 
            "likes":p.delikes_set.all().count(),
            "ganadores_total":p.participacion_set.filter(ganadora=True).count(),
            "ganadores_list":[
                {'nombre':g.usuario.username,
                'img':g.imagenuser()}
                 for g in p.participacion_set.filter(ganadora=True)],
            "orden":p.orden, 
            "dinamica":p.dinamica,
            "categorias":p.categorias,
            "segmentos":p.segmentos, 
            "pk": p.pk, 
            }
            promos.append(promomas)  

        promos = {'dinamicas':promos,'totales':len(promos)}
        return JsonResponse(promos)

promoEnd = promoEnd.as_view()



class promoSear(View,TimeMets):


    def get(self,request):
        import locale
        locale.setlocale(2, '')

        data = request.GET.copy()

        hoy = datetime.datetime.now() #+ datetime.timedelta(hours=22)
        upk = data.get('upk',None)
        search = {}

        word_sr = data.get('search',None)
        ciudad = data.get('ciudad',None)
        destacados = data.get('destacados',None)
        qs = []

        if word_sr:
            qs = [Q(categorias__icontains=word_sr)]

        if ciudad:
            qs = [Q(ciudad__icontains=ciudad)]


        if destacados:
            dests = {'true':True,'false':False}
            qs.append(Q(destacado=dests[destacados]))


        qs.append( Q(fecha_publicacion__isnull=True) | Q(fecha_publicacion__lte=hoy) )

        host = request.get_host()
    
        prox = Q(status='proximamente')
        pu = Q(status='publish') & Q(vigencia__gte=hoy)
        filtro = Q(prox | (pu))

        prms = Promocion.objects.filter(filtro).order_by('-destacado','fecha_evento','vigencia')
        prms = prms.filter(*qs)
        promos = [ 


                    {
                    'liked':p.yo_like(upk),   
                    "vigencia":self.fecha_to_str(p.vigencia), 
                    "vigencia":self.fecha_to_str(p.fecha_evento), 
                    "vigenciaUTC": time.mktime(p.vigencia.timetuple()),
                    "dia_evento":self.fecha_to_str(p.fecha_evento,formato='%d'),
                    "mes_evento":self.fecha_to_str(p.fecha_evento,formato='%b'),                    
                    'imagen':'https://%s%s'%(host,p.img), 
                    "titulo": p.linea_uno,
                    'status':p.status,
                    'ciudad':p.ciudad,
                    'lugar':p.lugar,
                    "titulo_color": p.linea_dos,
                    "titulo_completo":'%s %s'%(p.linea_uno,p.linea_dos), 
                    "participaciones":p.participacion_set.all().count(), 
                    "likes":p.delikes_set.all().count(),
                    "orden":p.orden, 
                    "dinamica":p.dinamica,
                    "categorias":p.categorias,
                    "segmentos":p.segmentos, 
                    "pk": p.pk, 
                    'participo':p.yaparticipo(upk)
                    }
                     for p in prms]

        promos = {'dinamicas':promos,'totales':len(promos)}

        return JsonResponse(promos)

promoSear = promoSear.as_view()


class promoDetail(View,TimeMets):


    def get(self,request,pks=None):
        mxtz = pytz.timezone('America/Mexico_City')       
        data = request.GET.copy()
        host = request.get_host()
        upk = data.get('upk',None)
        hoy = datetime.datetime.now(mxtz)
        if pks:

            ventaja = Pagesetts.objects.filter(fin__gte=hoy).order_by('fin').first()
            if ventaja:
                vtext = self.segments(ventaja.ventaja)
                ven = ventaja.ventaja
                texto = '%s al %s de %s'%(self.fecha_to_str(ventaja.inicio,formato='%d'),self.fecha_to_str(ventaja.fin,formato='%d'),self.fecha_to_str(ventaja.fin,formato='%B'))
                terminosventaja = ventaja.terminos
                
            else:
                ven = ''
                vtext = ''
                texto = ''
                terminosventaja = ''


            promo = Promocion.objects.get(pk=pks)


            dinamicas_names = {
                'trivia':'Trivia',
                'sopa':'Sopa de letras',
                'marcador_futbol':u'Marcador Fútbol',
                'puzzle':'Rompecabezas',
                'swiper':'Swiper',
            }


            prm = {
                    'liked':promo.yo_like(upk), 
                    'termsdin':promo.terminosdeladinamica(),
                    'descpdin':promo.descpdeladinamica(),
                    "vigencia":self.fecha_to_str(promo.vigencia), 
                    "fecha_publicacion_terminos":self.fecha_to_str(promo.fecha_publicacion,formato='%d de %B del %Y'),
                    "vigencia_terminos":self.fecha_to_str(promo.vigencia,formato='%d de %B del %Y'),
                    "fecha_evento":self.fecha_to_str(promo.fecha_evento),
                    "fecha_publicacion":self.fecha_to_str(promo.fecha_publicacion),
                    "dia_evento":self.fecha_to_str(promo.fecha_evento,formato='%d'),
                    "mes_evento":self.fecha_to_str(promo.fecha_evento,formato='%b'),                    
                    "ciudad":promo.ciudad,
                    'status':promo.status,
                    "lugar":promo.lugar,
                    "vigencia":self.fecha_to_str(promo.vigencia), 
                    "vigenciaUTC": self.fecha_timestamp_delay(promo.vigencia)+1,
                    'tiempoahora':self.fecha_timestamp(datetime.datetime.now(mxtz)),
                    'imagen':'https://%s%s'%(host,promo.img),
                    'imagen_ganadores':promo.finalimg(host), 
                    "descripcion_ganadores": promo.texto_alterno, 
                    "texto_ganadores":promo.header_final,
                    "bases": promo.bases, 
                    "imagen_lg":'https://%s%s'%(host,promo.imglg),
                    "imagen_lg_ganadores":'%s'%(promo.finalimg_min(host)),
                    "titulo": '%s %s'%(promo.linea_uno,promo.linea_dos),
                    "inicio_juego_txt":promo.titulo,
                    "shares":promo.participacion_set.all().count(), 
                    "likes": promo.delikes_set.all().count(), 
                    "categorias":promo.categorias,
                    "segmentos":promo.segmentos, 
                    "dinamica":promo.dinamica,
                    'premioterms':promo.premioterms,
                    'preguntas':promo.frontList(), 
                    "pk":promo.pk,
                    'terminosycondiciones':promo.terms,
                    "galeria":promo.galeria(host),
                    "ganadores_total":promo.participacion_set.filter(ganadora=True).count(),
                    "ganadores_list":[
                        {'nombre':g.usuario.username,
                        'img':g.imagenuser()}
                         for g in promo.participacion_set.filter(ganadora=True)],

                              }
            promos = {'promocion':prm,'ventaja':vtext,'ventajadesc':terminosventaja}

        else:
            promos = {'msg':'No hay promocion con ese ID'}

        return JsonResponse(promos)

promoDetail = promoDetail.as_view()



class rergUser(View):


    def get(self,request):
        data = request.GET.copy()
        
        usuario = data.get('u',None)

        if usuario and usuario!= 'undefined':

            u,failu = User.objects.get_or_create(email=data.get('u'),username=data.get('u'))
            u.first_name = data.get('name','Name')
            u.save()        
            response = {'userpk':u.pk}
        else:
            response = {'userpk':'no user'}

        return JsonResponse(response)

rergUser = rergUser.as_view()


class regTelUser(View,TimeMets):


    def get(self,request):
        data = request.GET.copy()
        
        usuario = data.get('correo',None)


        hoy = datetime.datetime.now()
        ventaja = Pagesetts.objects.filter(fin__gte=hoy).order_by('fin').first()
        if ventaja:
            vtext = self.segments(ventaja.ventaja)
            ven = ventaja.ventaja
            texto = '%s al %s de %s'%(self.fecha_to_str(ventaja.inicio,formato='%d'),self.fecha_to_str(ventaja.fin,formato='%d'),self.fecha_to_str(ventaja.fin,formato='%B'))
            
        else:
            ven = ''
            vtext = ''
            texto = ''



        if usuario:
            u,failu = User.objects.get_or_create(email=data.get('correo'),username=data.get('correo'))
            prof,failprof = Profileuser.objects.get_or_create(usuariopk=u)
            prof.nombre_usuario = u'%s'%(data.get('nombre','unName'))
            u.first_name = u'%s'%(data.get('nombre','unName'))[:30]
            u.save()        
            prof.save()
            response = {'userpk':u.pk,'ventaja':ven,'ventaja_texto':vtext,'fecha_ventaja':texto}
        else:
            response = {'userpk':'no user'}

        return JsonResponse(response)

regTelUser = regTelUser.as_view()



class settUser(View):


    def get(self,request):
        data = request.GET.copy()

        usuario = data.get('u',None)

        if usuario and usuario!= 'undefined':

            pu,failpu = Profileuser.objects.get_or_create(usuariopk_id=usuario)

            misservicios = []
            if pu.servicios:
                misservicios = pu.servicios

            if data.get('servicios') not in misservicios:
                pu.servicios = '%s,%s'%(pu.servicios,data.get('servicios'))
                pu.save()

            response = {'userpk':usuario,'servicios':pu.servicios}
        else:
            response = {'userpk':'no user'}

        return JsonResponse(response)

settUser = settUser.as_view()




class removeServiceUser(View):


    def get(self,request):
        data = request.GET.copy()

        usuario = data.get('u',None)

        if usuario and usuario!= 'undefined':

            pu,failpu = Profileuser.objects.get_or_create(usuariopk_id=usuario)

            misservicios = []
            servicio = data.get('servicios')

            if pu.servicios:
                misservicios = pu.servicios

            if servicio in misservicios:
                mis = misservicios.split(',')
                if servicio in mis:
                    noservicio = mis.index(servicio)
                    del mis[noservicio]
                    servs = ','.join(mis)
                    pu.servicios = servs
                    pu.save()

            response = {'userpk':usuario,'servicios':pu.servicios}
        else:
            response = {'userpk':'no user'}

        return JsonResponse(response)

removeServiceUser = removeServiceUser.as_view()



class getUser(View,TimeMets):

    def get(self,request):
        import locale
        locale.setlocale(2, '')


        hoy = datetime.datetime.now()
        ventaja = Pagesetts.objects.filter(fin__gte=hoy).order_by('fin').first()
        if ventaja:
            vtext = self.segments(ventaja.ventaja)
            ven = ventaja.ventaja
            texto = '%s al %s de %s'%(self.fecha_to_str(ventaja.inicio,formato='%d'),self.fecha_to_str(ventaja.fin,formato='%d'),self.fecha_to_str(ventaja.fin,formato='%B'))
            
        else:
            ven = ''
            vtext = ''
            texto = ''

        data = request.GET.copy()
        usuario = data.get('upk',None)
        if usuario=='no user':
            usuario = None

        hoy = datetime.datetime.now() + datetime.timedelta(hours=22)
        if usuario:
            ventaja = Pagesetts.objects.filter(fin__gte=hoy).order_by('fin').first()

            u = User.objects.get(pk=usuario)
            try:
                pu = u.profileuser_set.all().first()
                serviciosp = pu.servicios
                imagen = pu.imagen
            except:
                pu = None
                serviciosp = ''
                imagen = ''


            try:

                if ventaja.ventaja.replace('_','') in serviciosp:
                    ventajasi=1
                else:
                    ventajasi=0
            except:
                ventajasi = 0



            us = {
                'pk':u.pk,
                'ventaja':ventajasi,
                'email':u.email,
                'name':u.first_name,
                'servicios':serviciosp,
                'imagen':'%s'%(imagen),
                'fecha_ingreso':self.fecha_to_str(u.date_joined,formato='%x %X')
            }

        
            response = {'usuario':us,'ventaja':ven,'ventaja_texto':vtext,'fecha_ventaja':texto}
        else:
            us = {
                'pk':0,
                'ventaja':0,
                'email':'',
                'name':'',
                'servicios':'',
                'imagen':'%s'%(''),
                'fecha_ingreso':''
            }



            response = {'usuario':us,'ventaja':ven,'ventaja_texto':vtext,'fecha_ventaja':texto}

        return JsonResponse(response)

getUser = getUser.as_view()



class getProfileUser(View,TimeMets):

    def get(self,request):

        data = request.GET.copy()
        usuario = data.get('upk',None)

        if usuario:

            u = User.objects.get(pk=usuario)
            pu,failpu = Profileuser.objects.get_or_create(usuariopk_id=usuario)
            hoy = datetime.datetime.now()

            us = {
                'pk':u.pk,
                'email':u.email,
                'name':u.first_name,
                'servicios':pu.servicios,
                'imagen':'%s'%(pu.imagen),
                'likes':[
                    {
                    'promopk':li.promopk.pk,
                    'imagen':li.promopk.img,
                    "dia_evento":self.fecha_to_str(li.promopk.fecha_evento,formato='%d'),
                    "mes_evento":self.fecha_to_str(li.promopk.fecha_evento,formato='%b'),
                    "fecha_vigencia":self.fecha_to_str(li.promopk.vigencia,formato='%d |%b. %Y'),                                        
                    "ciudad":li.promopk.ciudad,
                    'status':li.promopk.status,
                    'vigencia':li.promopk.activaono(),
                    'titulo':'%s %s'%(li.promopk.linea_uno,li.promopk.linea_dos),

                    }
                    for li in u.delikes_set.filter(promopk__status__in=['publish','finalizado','proximamente'],promopk__vigencia__gte=hoy)
                ],
                'participaciones':[
                    {
                    'promopk':parti.promopk.pk,
                    'imagen':parti.promopk.img,
                    "dia_evento":self.fecha_to_str(parti.promopk.fecha_evento,formato='%d'),
                    "mes_evento":self.fecha_to_str(parti.promopk.fecha_evento,formato='%b'),
                    "fecha_vigencia":self.fecha_to_str(parti.promopk.vigencia,formato='%d |%b. %Y'),                                        
                    "ciudad":parti.promopk.ciudad,
                    'status':parti.promopk.status,
                    'vigencia':parti.promopk.activaono(),
                    'titulo':'%s %s'%(parti.promopk.linea_uno,parti.promopk.linea_dos),
                    
                    }
                     for parti in u.participacion_set.filter(promopk__status__in=['publish','finalizado','proximamente'],promopk__vigencia__gte=hoy,final__isnull=False)
                ]

            }

        
            response = {'usuario':us}
        else:
            response = {'userpk':'no user'}

        return JsonResponse(response)

getProfileUser = getProfileUser.as_view()








class Cats(View):

    def get(self,request):
        mxtz = pytz.timezone('America/Mexico_City')
        hoy = datetime.datetime.now(mxtz)
        qq = (Q(promocion__fecha_publicacion__isnull=True) | Q(promocion__fecha_publicacion__lte=hoy)) & Q(promocion__vigencia__gte=hoy)
        categorias = Catpromo.objects.filter(qq).values_list('categoria__catslug',flat=True).distinct()
        #categorias = Catpromo.objects.values_list('categoria__catslug',flat=True).distinct()

        cats = Promocat.objects.filter(catslug__in=categorias)

        categories = [
            {'pk':x.pk,
             'catslug':x.catslug,
             'catname':x.catname
            }
            for x in cats
        ]

        response = {'categorias':categories}
        return JsonResponse(response)

Cats = Cats.as_view()



class getRows(View):

    def get(self,request):
        data = request.POST.copy()
        m = Wpage.objects.filter(ishome=True).first()

        modulos = m.getmodulos()
        jsmodules = simplejson.loads(modulos)
        items = jsmodules

        response = {'items':items}
        return JsonResponse(response)

getRows = getRows.as_view()






#al inicio de la dinamica
class Participandome(View,TimeMets):

    def get(self,request,uspk=None,promopk=None):
        response = {}
        data = request.GET.copy()

        if uspk and promopk:

            if data.get('check',None):
                part = Participacion.objects.filter(usuario_id=uspk,promopk_id=promopk).first()
                if part:
                    if part.final:
                        response['status'] = 'finalizo'
                    else:
                        response['status'] = 'progress'
                else:
                    response['status'] = 'progress'

                return JsonResponse(response)


            user = User.objects.get(pk=uspk)
            promo = Promocion.objects.get(pk=promopk)
            parti,yaparticipo = Participacion.objects.get_or_create(usuario=user,promopk=promo)
            mxtz = pytz.timezone('America/Mexico_City')
            hoy = datetime.datetime.now(mxtz)
            parti.inicio = hoy
            parti.save()
            fechainicio = hoy            

            try:
                promopreguntas = promo.pregunta_set.all().first()
                promopreguntasresp = promopreguntas.respuesta_set.filter(cor=True).first()
                p = promopreguntasresp.pk

            except: 
                p = 0

            response = {'partipk':parti.pk,
                        'inicio_p':p,
                        'nivel_respuestas':parti.nivelanswer,
                        'inicio':self.fecha_to_str(fecha=datetime.datetime.now(),formato='%x %X'),
                        'inicioUTC':self.fecha_timestamp(fecha=fechainicio)

             }
            
            if yaparticipo:
                response['status']='inicio'
            else:
                if parti.final:
                    response['status'] = 'finalizo'
                else:
                    response['status'] = 'progress'

        else:
            response = {'pk':'no hay participation que registrar'}

        return JsonResponse(response)

Participandome = Participandome.as_view()



#al inicio de la dinamica
class Finalpanorama(View,TimeMets):

    def get(self,request,uspk=None,promopk=None):

        response = {}

        if uspk and promopk:
            user = User.objects.get(pk=uspk)
            promo = Promocion.objects.get(pk=promopk)
            parti,yaparticipo = Participacion.objects.get_or_create(usuario=user,promopk=promo)
            parti.final = datetime.datetime.now()
            parti.save()
            response = {'partipk':parti.pk,
                        'nivel_respuestas':parti.nivelanswer,
                        'inicio':self.fecha_to_str(fecha=parti.inicio,formato='%x %X'),
                        'inicioUTC':self.fecha_timestamp(fecha=parti.inicio),
            'final':self.fecha_to_str(fecha=parti.final,formato='%x %X'),
            'finalUTC':self.fecha_timestamp(fecha=parti.final)
             }
            

        else:
            response = {'pk':'no hay participation que registrar'}

        return JsonResponse(response)

Finalpanorama = Finalpanorama.as_view()




#al inicio de la dinamica
class FinalTrivia(View,TimeMets):

    def get(self,request):
        mxtz = pytz.timezone('America/Mexico_City')
        context = {}
        data = request.GET.copy()
        uspk = data.get('uspk',None)
        promo = Promocion.objects.get(pk=data.get('promo'))
        fecha_aviso = promo.vigencia + datetime.timedelta(hours=24)
        parti = Participacion.objects.get(promopk=promo,usuario=User.objects.get(pk=uspk))
        parti.tiempo = '%s:%s'%(data.get('mins','0'),data.get('segs'))       
        parti.save()
        respuestas = request.GET.getlist('pregunta')
        parti.resparticipacion_set.all().delete()
        correctas = 0

        for r in respuestas:
            
            anser = 'resp_%s'%(r)
            respues = Respuesta.objects.get(pk=data.get(anser))
            if respues.cor=='True':
                correctas = correctas + 1
            rx = Resparticipacion()
            rx.parti = parti
            rx.pregunta = r
            rx.respuesta = data.get(anser)
            rx.save()

        total = data.get('tiempo','10:0:0')
        parti.nivelanswer = correctas
        parti.final = datetime.datetime.now(mxtz)
        parti.tiempo = total
        parti.save()
        fecha_aviso = self.fecha_to_str(fecha_aviso)

        response = {'correctas':parti.nivelanswer,
                    'tiempo':data.get('tiempo','0:0:0'),
                    'tiempoUTC':total,
                    'aviso_ganadores':fecha_aviso,
                    'inicio':parti.inicio,
                    'final':parti.final

                    }
        return JsonResponse(response)



FinalTrivia = FinalTrivia.as_view()





#al inicio de la dinamica
class FinalPalabras(View,TimeMets):
    
    def get(self,request):
        context = {}
        data = request.GET.copy()
        mxtz = pytz.timezone('America/Mexico_City')        
        uspk = data.get('uspk',None)
        promo = Promocion.objects.get(pk=data.get('promo'))
        parti = Participacion.objects.get(promopk=promo,usuario=User.objects.get(pk=uspk))

        parti.tiempo = '%s:%s'%(data.get('mins','0'),data.get('segs'))
        parti.save()
        respuestas = request.GET.getlist('pregunta')
        parti.respondepalabras_set.all().delete()
        correctas = 0

        for r in respuestas:
            anser = 'resp_%s'%(r)
            respues = Dinpalabra.objects.get(pk=r)

            if respues.palabra.lower()==data.get(anser).lower():
                correctas = correctas + 1
            rx = Respondepalabras()
            rx.parti = parti
            rx.pregunta = r
            rx.respuesta = data.get(anser).lower()
            rx.save()


        parti.nivelanswer = correctas
        parti.final = datetime.datetime.now(mxtz)
        parti.save()

        inicio = self.fecha_timestamp(parti.inicio)
        final = self.fecha_timestamp(parti.final)
        total = final - inicio
        parti.tiempo = total
        parti.save()

        response = {'pk':'newpk','correctas':parti.nivelanswer,'tiempoUTC':total}
        return JsonResponse(response)



FinalPalabras = FinalPalabras.as_view()







#al inicio de la dinamica
class FinalFutbol(View,TimeMets):
    
    def get(self,request):
        
        context = {}
        data = request.GET.copy()
        mxtz = pytz.timezone('America/Mexico_City')
        uspk = data.get('uspk',None)
        promo = Promocion.objects.get(pk=data.get('promo'))
        parti = Participacion.objects.get(promopk=promo,usuario=User.objects.get(pk=uspk))

        parti.tiempo = '%s:%s'%(data.get('mins','0'),data.get('segs'))
        parti.save()
        respuestas = request.GET.getlist('pregunta')
        parti.respondefutbol_set.all().delete()
        correctas = 0


        parti.final = datetime.datetime.now(mxtz)
        parti.save()

        for r in respuestas:
            anser = 'resp_%s'%(r)
            marcador_uno = 'marcador_uno_%s'%(r)
            marcador_dos = 'marcador_dos_%s'%(r)
            respues = Dinfutbol.objects.get(pk=r)

            if respues.respuesta.lower()==data.get(anser).lower():
                correctas = correctas + 1
            rx = Respondefutbol()
            rx.dinfut = parti
            rx.marcador_uno = data.get(marcador_uno)
            rx.marcador_dos = data.get(marcador_dos)
            rx.respuesta = data.get(anser).lower()
            rx.save()


        parti.nivelanswer = correctas
        parti.final = datetime.datetime.now(mxtz)
        parti.save()

        #inicio = self.fecha_timestamp(parti.inicio)
        #final = self.fecha_timestamp(parti.final)
        total = final - inicio
        parti.tiempo = total
        parti.save()

        response = {'pk':'newpk','correctas':parti.nivelanswer,'tiempoUTC':total}
        return JsonResponse(response)



FinalFutbol = FinalFutbol.as_view()



#al inicio de la dinamica
class addLike(View,TimeMets):
    
    def get(self,request):
        context = {}
        data = request.GET.copy()
        userpk = data.get('upk',None)
        promopk = data.get('ppk',None)
        likes = None

        if userpk and promopk and userpk!='undefined':
            userpk = User.objects.get(pk=userpk)
            promopk = Promocion.objects.get(pk=promopk)
            liker,nuevo = Delikes.objects.get_or_create(userpk=userpk,promopk=promopk)
            likes = promopk.delikes_set.all().count()
        else:
            promopk = Promocion.objects.get(pk=promopk)
            likes = promopk.delikes_set.all().count()

        response = {'likes':likes}
        return JsonResponse(response)



addLike = addLike.as_view()



#al inicio de la dinamica
class FinalSopa(View,TimeMets):
    
    def get(self,request,uspk=None,promopk=None):

        context = {}
        data = request.GET.copy()
        response = {} 
        mxtz = pytz.timezone('America/Mexico_City')
        promo = Promocion.objects.get(pk=promopk)
        parti = Participacion.objects.get(promopk=promopk,usuario=User.objects.get(pk=uspk))
        parti.final = datetime.datetime.now(mxtz)
        parti.nivelanswer = data.get('respuestas',0)
        total = data.get('tiempo','0:0:0')
        parti.tiempo = total
        parti.save()
        response = {'pk':'newpk','correctas':parti.nivelanswer,'tiempoUTC':total}
        return JsonResponse(response)

FinalSopa = FinalSopa.as_view()



#al inicio de la dinamica
class FinalPuzz(View,TimeMets):
    
    def get(self,request,uspk=None,promopk=None):

        context = {}
        data = request.GET.copy()
        response = {} 
        mxtz = pytz.timezone('America/Mexico_City')
        promo = Promocion.objects.get(pk=promopk)
        parti = Participacion.objects.get(promopk=promopk,usuario=User.objects.get(pk=uspk))
        parti.final = datetime.datetime.now(mxtz)
        parti.nivelanswer = data.get('respuestas',0)
        total = data.get('tiempo','0:0:0')
        parti.tiempo = total
        parti.save()
        response = {'pk':'newpk','correctas':parti.nivelanswer,'tiempoUTC':total}
        return JsonResponse(response)
FinalPuzz = FinalPuzz.as_view()


class FinalSwip(View,TimeMets):
    def get(self,request,uspk=None,promopk=None):
        context = {}
        data = request.GET.copy()
        response = {} 
        nivel = 0
        cuantas = 0
        mxtz = pytz.timezone('America/Mexico_City')
        promo = Promocion.objects.get(pk=promopk)
        parti = Participacion.objects.get(promopk_id=promopk,usuario_id=uspk)

        for d in data:
            cuantas +=1
            datos = data.get(d,None)
            if datos:
                datos = simplejson.loads(datos)
                swimg = Swipimages.objects.get(pk=datos['imgpk'])
                if swimg.sideimg==datos['responde']:
                    nivel+=1
        parti.final = datetime.datetime.now(mxtz)
        parti.nivelanswer = nivel
        total = data.get('tiempo','0:0:0')
        parti.tiempo = total
        parti.save()

        response = {'pk':'newpk','correctas':parti.nivelanswer,'tiempoUTC':total,'totals':cuantas}

        
        return JsonResponse(response)


FinalSwip = FinalSwip.as_view()






#al inicio de la dinamica

@csrf_exempt
def fotoPerfil(request):
    archivo = request.FILES['archivo1']
    upk = request.POST.get('upk',None)
    tempcrop = StringIO.StringIO()
    imagen = Image.open(archivo)
    for orientation in ExifTags.TAGS.keys():
        if ExifTags.TAGS[orientation]=='Orientation':
            break    

    try:
        exif=dict(imagen._getexif().items())
        if exif[orientation] == 3:
            imagen=imagen.rotate(180, expand=True)
        elif exif[orientation] == 6:
            imagen=imagen.rotate(270, expand=True)
        elif exif[orientation] == 8:
            imagen=imagen.rotate(90, expand=True)
    except:
        pass


    imagen.save(tempcrop,format='PNG',dpi=(72,72))
    #assert False,imagen
    cropsafe = ContentFile(tempcrop.getvalue(),'perfil_%s.png'%(upk))

    if upk:
        usuario = Profileuser.objects.get(usuariopk_id=upk)
        usuario.imagen = cropsafe
        usuario.save()
        imagens = 'https://admin.experienciastelcel.com/%s'%usuario.imagen

    response = {'upk':upk,'img':imagens}
    response = simplejson.dumps(response)
    return HttpResponse(response)



