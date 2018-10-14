# -*- coding: utf-8 -*-

#from django.http import HttpResponse
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
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.files import File

from base64 import b64decode
import StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile

import datetime
import pytz


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

    def strfecha(self,fecha=None):
        try: 
            fechastr = datetime.datetime.strptime(fecha, '%b. %d | %Y')
        except:
            fechastr = None            
        return fechastr


    def segments(self,slug=None):
        segmentos = {
        'clarovideo':'Claro Video',
        'claromusica':u'Claro Música',
        'clarojuegos':'Claro Juegos',
        'clasrodrive':'Claro Drive',
        'clubclaroapp':'Club Claro app',
        'claroentretenimiento':'Claro Entretenimiento',
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
        import locale
        locale.setlocale(2, '')
        data = request.GET.copy()        
        search = {}
        word_sr = data.get('search',None)
        destacados = data.get('destacados',None)
        qs = [] 
        if word_sr:
            qs = [Q(linea_uno__icontains=word_sr) | Q(linea_dos__icontains=word_sr) | Q(linea_tres__icontains=word_sr)]
        if destacados:
            dests = {'true':True,'false':False}
            qs.append(Q(destacado=dests[destacados.lower()]))

        hoy = datetime.datetime.now() + datetime.timedelta(hours=22)
        qs.append( Q(fecha_publicacion__isnull=True) | Q(fecha_publicacion__lte=hoy) )
        host = request.get_host()
        todos = Promocion.objects.filter(status__in=['publish','proximamente'],vigencia__gte=hoy).order_by('-destacado','orden','-vigencia',)
        prms = todos.filter(*qs)

        subtotales = prms.count()

        if destacados and subtotales>0:
            if destacados.lower()=='true':
                if subtotales<3:
                    faltantes = 3 - subtotales
                    extras = todos[0:faltantes]

                    prms = todos[0:3]
                else:
                    prms = prms[0:3]

        promos = [ 
                    {   
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
                    }
                     for p in prms]

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

        promos = {'dinamicas':promos,'totales':len(promos),'ventaja':ven,'ventaja_texto':vtext,'fecha_ventaja':texto}
        return JsonResponse(promos)

promoList = promoList.as_view()



class promoEnd(View,TimeMets):

    def get(self,request):
        import locale
        locale.setlocale(2, '')

        data = request.GET.copy()

        hoy = datetime.datetime.now() 
        
        host = request.get_host()
        prms = Promocion.objects.filter(status__in=['publish','proximamente'],vigencia__lte=hoy).order_by('-vigencia')
        #prms = prms.filter(*qs)
        promos = [ 
                    {   
                    "vigencia":self.fecha_to_str(p.vigencia), 
                    "fecha_evento":self.fecha_to_str(p.fecha_evento),
                    "fecha_publicacion":self.fecha_to_str(p.fecha_publicacion),
                    "dia_evento":self.fecha_to_str(p.fecha_evento,formato='%d'),
                    "mes_evento":self.fecha_to_str(p.fecha_evento,formato='%b'),
                    'ciudad':p.ciudad,
                    'status':p.status,
                    'lugar':p.lugar, 
                    "vigenciaUTC": time.mktime(p.vigencia.timetuple()),
                    'imagen':'https://%s%s'%(host,p.img),
                    'imagen_ganadores':p.finalimg(host), 
                    "titulo": p.linea_uno,
                    "titulo_color": p.linea_dos,
                    "titulo_completo":'%s %s'%(p.linea_uno,p.linea_dos), 
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

        promos = {'dinamicas':promos,'totales':len(promos)}
        return JsonResponse(promos)

promoEnd = promoEnd.as_view()



class promoSear(View,TimeMets):


    def get(self,request):
        import locale
        locale.setlocale(2, '')

        data = request.GET.copy()

        hoy = datetime.datetime.now() + datetime.timedelta(hours=22)
        
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
        prms = Promocion.objects.filter(status__in=['publish','proximamente'],vigencia__gte=hoy)
        prms = prms.filter(*qs)
        promos = [ 


                    {   
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
                    }
                     for p in prms]

        promos = {'dinamicas':promos,'totales':len(promos)}

        return JsonResponse(promos)

promoSear = promoSear.as_view()


class promoDetail(View,TimeMets):


    def get(self,request,pks=None):
        import locale
        locale.setlocale(2,'')        
        data = request.GET.copy()
        host = request.get_host()

        if pks:
            promo = Promocion.objects.get(pk=pks)
            prm = {
                    "vigencia":self.fecha_to_str(promo.vigencia), 
                    "fecha_evento":self.fecha_to_str(promo.fecha_evento),
                    "dia_evento":self.fecha_to_str(promo.fecha_evento,formato='%d'),
                    "mes_evento":self.fecha_to_str(promo.fecha_evento,formato='%b'),                    
                    "ciudad":promo.ciudad,
                    'status':promo.status,
                    "lugar":promo.lugar,
                    "vigencia":self.fecha_to_str(promo.vigencia), 
                    "vigenciaUTC": self.fecha_timestamp(promo.vigencia),
		            'tiempoahora':self.fecha_timestamp(datetime.datetime.now()),
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
                    'preguntas':promo.frontList(), 
                    "pk":promo.pk,
                    "galeria":promo.galeria(host),
                    "ganadores_total":promo.participacion_set.filter(ganadora=True).count(),
                    "ganadores_list":[
                        {'nombre':g.usuario.username,
                        'img':g.imagenuser()}
                         for g in promo.participacion_set.filter(ganadora=True)],

                              }
            promos = {'promocion':prm}

        else:
            promos = {'msg':'No hay promocion con ese ID'}

        return JsonResponse(promos)

promoDetail = promoDetail.as_view()



class rergUser(View):

    def get(self,request):
        data = request.GET.copy()
        usuario = data.get('u',None)

        if usuario:

            u,failu = User.objects.get_or_create(email=data.get('u'),username=data.get('u'))
            u.first_name = data.get('name','Name')
            u.save()

            pu,failpu = Profileuser.objects.get_or_create(usuariopk=u)
            pu.servicios = data.get('servicios')
            pu.save()
        
            response = {'userpk':u.pk,'servicios':pu.servicios}
        else:
            response = {'userpk':'no user'}

        return JsonResponse(response)

rergUser = rergUser.as_view()


class getUser(View,TimeMets):

    def get(self,request):
        import locale
        locale.setlocale(2, '')

        data = request.GET.copy()
        usuario = data.get('upk',None)
        hoy = datetime.datetime.now() + datetime.timedelta(hours=22)
        if usuario:
            ventaja = Pagesetts.objects.filter(fin__gte=hoy).order_by('fin').first()

            u = User.objects.get(pk=usuario)
            pu = u.profileuser_set.all().first()

            if ventaja.ventaja.replace('_','') in pu.servicios:
                ventajasi=1
            else:
                ventajasi=0


            us = {
                'pk':u.pk,
                'ventaja':ventajasi,
                'email':u.email,
                'name':u.first_name,
                'servicios':pu.servicios,
                'imagen':'%s'%(pu.imagen),
                'fecha_ingreso':self.fecha_to_str(u.date_joined,formato='%x %X')
            }

        
            response = {'usuario':us}
        else:
            response = {'userpk':'no user'}

        return JsonResponse(response)

getUser = getUser.as_view()



class getProfileUser(View):

    def get(self,request):
        import locale
        locale.setlocale(2, '')

        data = request.GET.copy()
        usuario = data.get('upk',None)

        if usuario:

            u = User.objects.get(pk=usuario)
            pu = u.profileuser_set.all().first()


            us = {
                'pk':u.pk,
                'email':u.email,
                'name':u.first_name,
                'servicios':pu.servicios,
                'imagen':'%s'%(pu.imagen),
                'likes':[
                    {
                    'promopk':li.pk,
                    'imagen':li.promopk.img,
                    'titulo':'%s %s'%(li.promopk.linea_uno,li.promopk.linea_dos),

                    }
                     for li in u.delikes_set.all()
                ],
                'participaciones':[
                    {
                    'promopk':parti.pk,
                    'imagen':parti.promopk.img,
                    'titulo':'%s %s'%(parti.promopk.linea_uno,parti.promopk.linea_dos),
                    
                    }
                     for parti in u.participacion_set.all()
                ]

            }

        
            response = {'usuario':us}
        else:
            response = {'userpk':'no user'}

        return JsonResponse(response)

getProfileUser = getProfileUser.as_view()








class Cats(View):

    def get(self,request):
        hoy = datetime.datetime.now()
        qq = Q(promocion__fecha_publicacion__isnull=True) | Q(promocion__fecha_publicacion__gte=hoy)
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

        if uspk and promopk:
            user = User.objects.get(pk=uspk)
            promo = Promocion.objects.get(pk=promopk)
            parti,yaparticipo = Participacion.objects.get_or_create(usuario=user,promopk=promo)

            mxtz = pytz.timezone('America/Mexico_City')
            fechainicio = parti.inicio.astimezone(mxtz)            



            response = {'partipk':parti.pk,
                        'nivel_respuestas':parti.nivelanswer,
                        'inicio':self.fecha_to_str(fecha=fechainicio,formato='%x %X'),
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


        parti.nivelanswer = correctas
        parti.final = datetime.datetime.now()
        parti.save()

        inicio = self.fecha_timestamp(parti.inicio)
        final = self.fecha_timestamp(parti.final)
        fecha_aviso = self.fecha_to_str(fecha_aviso)
        total = final - inicio
        parti.tiempo = total
        parti.save()

        response = {'correctas':parti.nivelanswer,'tiempoUTC':total,'aviso_ganadores':fecha_aviso}
        return JsonResponse(response)



FinalTrivia = FinalTrivia.as_view()





#al inicio de la dinamica
class FinalPalabras(View,TimeMets):
    
    def get(self,request):
        context = {}
        data = request.GET.copy()
 
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
        parti.final = datetime.datetime.now()
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
 
        uspk = data.get('uspk',None)
        promo = Promocion.objects.get(pk=data.get('promo'))
        parti = Participacion.objects.get(promopk=promo,usuario=User.objects.get(pk=uspk))

        parti.tiempo = '%s:%s'%(data.get('mins','0'),data.get('segs'))
        parti.save()
        respuestas = request.GET.getlist('pregunta')
        parti.respondefutbol_set.all().delete()
        correctas = 0


        parti.final = datetime.datetime.now()
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
        parti.final = datetime.datetime.now()
        parti.save()

        inicio = self.fecha_timestamp(parti.inicio)
        final = self.fecha_timestamp(parti.final)
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

        if userpk and promopk:
            userpk = User.objects.get(pk=userpk)
            promopk = Promocion.objects.get(pk=promopk)
            liker,nuevo = Delikes.objects.get_or_create(userpk=userpk,promopk=promopk)
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

        promo = Promocion.objects.get(pk=promopk)
        parti = Participacion.objects.get(promopk=promopk,usuario=User.objects.get(pk=uspk))

        #parti.tiempo = '%s:%s'%(data.get('mins','0'),data.get('segs'))
        #parti.save()
        parti.final = datetime.datetime.now()
        parti.nivelanswer = data.get('respuestas',0)
        parti.save()



        inicio = self.fecha_timestamp(parti.inicio)
        final = self.fecha_timestamp(parti.final)
        total = final - inicio
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

        promo = Promocion.objects.get(pk=promopk)
        parti = Participacion.objects.get(promopk=promopk,usuario=User.objects.get(pk=uspk))

        #parti.tiempo = '%s:%s'%(data.get('mins','0'),data.get('segs'))
        #parti.save()
        parti.final = datetime.datetime.now()
        parti.nivelanswer = data.get('respuestas',0)
        parti.save()

        inicio = self.fecha_timestamp(parti.inicio)
        final = self.fecha_timestamp(parti.final)
        total = final - inicio
        parti.tiempo = total
        parti.save()

        response = {'pk':'newpk','correctas':parti.nivelanswer,'tiempoUTC':total}

        
        return JsonResponse(response)


FinalPuzz = FinalPuzz.as_view()