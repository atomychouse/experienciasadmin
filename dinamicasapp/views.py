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
from django.core.mail import send_mail, BadHeaderError
from django.core.exceptions import ValidationError
from .models import * 
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.template.defaultfilters import slugify
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
from dinamicasapp.models import * 
from motorapp.models import * 
from datetime import datetime
import locale
from mobapp.views import TimeMets
from PIL import Image
from io import BytesIO
import StringIO
from django.core.files.base import ContentFile
import locale


def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj




class addPromo(View):

  def post(self,request):
    data = request.POST.copy()
    locale.setlocale(2, '')
    data['img']=data.get('media[firstimg]','').split('?')[0]
    data['imglg']=data.get('media[imglg]','').split('?')[0]
    segmentos = request.POST.getlist('segmentos[]')
    categorias = request.POST.getlist('categorias[]')
    data['segmentos'] = simplejson.dumps(segmentos)
    data['categorias'] = simplejson.dumps(categorias)
    data['slug_titulo'] = slugify(data.get('slug_titulo','telcel es la red'))


    pk = data.get('pk','0')

    if pk=='0':
      p = None
    else:
      p = Promocion.objects.get(pk=pk)

    try:
      fecha = datetime.strptime(data.get('vigencia'), '%d/%m/%Y')
    except:
      fecha = None
      
    try: 
      fecha_evento = datetime.strptime(data.get('fecha_evento'),'%d/%m/%Y')
    except:
      fecha_evento = None

    try: 
      fecha_publicacion = datetime.strptime(data.get('fecha_publicacion'), '%d/%m/%Y')
    except:
      fecha_publicacion = None


    data['vigencia'] = fecha
    data['fecha_evento'] = fecha_evento
    data['fecha_publicacion'] = fecha_publicacion

    f = FormCreator()
    forma = f.form_to_model(modelo=Promocion,excludes=[])
    forma = forma(data,instance=p)

    if forma.is_valid():
      saved = forma.save()
      newpk = saved.pk
      
      pcat = Promocat.objects.filter(catslug__in=categorias)
      if pcat:
        saved.catpromo_set.all().delete()
        for pc in pcat:
          newcat = Catpromo(promocion=saved,categoria=pc)
          newcat.save()

    else:
      assert False,forma.errors


    response = {'pk':newpk}
    return JsonResponse(response)


addPromo = addPromo.as_view()


class rmPromo(View):

  def post(self,request):
    data = request.POST.copy()

    if data.get('pk',None):
      p = Promocion.objects.get(pk=data.get('pk'))
      p.delete()
      response = {'pk':'deleted'}
    else:
      response = {'pk':'no deleted'}


    return JsonResponse(response)


rmPromo = rmPromo.as_view()



class addFoto(View):

  def post(self,request):
    data = request.POST.copy()
    cropimg = data.get('img')
    img,crop = cropimg.split(';base64,')
    imagen = crop.decode('base64')
    croped = Image.open(BytesIO(imagen))
    tempcrop = StringIO.StringIO()
    croped.save(tempcrop,format='PNG',dpi=(72,72))
    name_imagen = 'crop_%s.%s'%(data.get('pk'),croped.format.lower())        
    cropsafe = ContentFile(tempcrop.getvalue(),name_imagen)



    if data.get('pk',None):
      p = Pregunta.objects.get(pk=data.get('pk'))
      
      p.imagen = cropsafe
      p.save()

      response = {'pk':'deleted'}
    else:
      response = {'pk':'no deleted'}


    return JsonResponse(response)


addFoto = addFoto.as_view()



class rmQuiz(View):

  def post(self,request):
    data = request.POST.copy()

    if data.get('pk',None):
      p = Pregunta.objects.get(pk=data.get('pk'))
      p.delete()
      response = {'pk':'deleted'}
    else:
      response = {'pk':'no deleted'}


    return JsonResponse(response)


rmQuiz = rmQuiz.as_view()




class saveQuiz(View):

  def post(self,request):

    response = {}
    data = request.POST.copy()
    options = request.POST.getlist('options[]')

    assert False,options

    promopk = data.get('promopk',None)
    pk = data.get('pk','0')
    if promopk:
      promo = Promocion.objects.get(pk=promopk)
      if pk=='0':
        preg = Pregunta()
      else: 
        preg = Pregunta.objects.get(pk=pk)
        preg.respuesta_set.all().delete()

      preg.owners = promo
      preg.pregunta = data.get('pregunta')
      preg.orden = data.get('orden',1)

      preg.save()

      response['preg']=preg.pk

      for x in options:
        opt = simplejson.loads(x)
        res = Respuesta()
        res.resp=opt['texto']
        res.indice = opt['indice']        
        res.pregunta = preg
        res.cor = opt.get('cor')
        res.save()

    return JsonResponse(response)



  def get(self,request):
    response = {}
    data = request.GET.copy()
    options = request.GET.getlist('options')



    promopk = data.get('promopk',None)
    pk = data.get('pk','0')
    if promopk:
      promo = Promocion.objects.get(pk=promopk)
      if pk=='0':
        preg = Pregunta()
      else: 
        preg = Pregunta.objects.get(pk=pk)
        preg.respuesta_set.all().delete()

      preg.owners = promo
      preg.pregunta = data.get('pregunta')
      preg.orden = data.get('orden',1)

      preg.save()

      response['preg']=preg.pk

      for x in options:
        opt = simplejson.loads(x)
        res = Respuesta()
        res.resp=opt['texto']
        res.indice = opt['indice']        
        res.pregunta = preg
        res.cor = opt.get('cor')
        res.save()

    return JsonResponse(response)


saveQuiz = saveQuiz.as_view()



class Index(View):

    template = 'dinamicasapp/index.html'

    def get(self, request,pk=None,section=None,column=None,subsection=None):

        data = request.GET.copy()
        context = {}

        if section and not column and not subsection:
            search = {'parentpage__isnull':True,'slug':section}
        if column:
            search = {'columna__catslug':column,'parentpage__slug':section,'slug':subsection}

        if not section:
            search = {'ishome__isnull':False}

        curr_page = Wpage.objects.filter(slug='dinamicas_system').first()
        #curr_page.filter(**search)

        pages   = Wpage.objects.filter(parentpage__isnull=True)
        userp = {'name':'Alberto','profile':'admin'}

        pages = [
            {'pagepk':p.pk,
             'page_name':p.name,
             'page_slug':p.slug,
             'orden':p.orden,
             'secs':[{'colpk':cat.pk,
                      'colname':cat.catname,
                      'colslug':cat.catslug,
                      'orden':cat.orden,
                      'secs':[{'pagepk':subp.pk,
                               'page_name':subp.name,
                               'page_slug':subp.slug

                            } for subp in cat.wpage_set.all()]

                      } for cat in p.catpage_set.all()]

             }

              for p in pages]

        context['cur_page'] = curr_page
        context['user'] = userp
        context['pages'] = simplejson.dumps(pages)
        context['dinamicas'] = Dinamica.objects.all()
        
        


        response = render(request, self.template, context)
        return response

Index = Index.as_view()



class addDinamica(View):

    template = 'dinamicasapp/adddinamica.html'

    def get(self, request,pk=None):
        data = request.GET.copy()
        context = {}

        if pk:
          d = Dinamica.objects.get(pk=pk)

          dee = d.mediadim_set.all().last()
          if dee:
            img = dee.myimg.name
          else:
            img = 'static/statics/imgs/defaults/imgrebase.png'

          dina = {
              'dpk':d.pk,
              'bkcolor':d.bkcolor,
              'inicia':d.inicia,
              'finaliza':d.finaliza,
              'titulo':d.titulo,
              'bases':d.bases,
              'din_params':{
                'inicial':{'img':'/static/statics/imgs/defaults/gridlink.png','titulo':'TITULO','texto':'<p>INICIO</p>'},
                'final':{'img':'/static/statics/imgs/defaults/gridlink.png','titulo':'TITULO','texto':'<p>INICIO</p>'}
              },
              'media':{'img':'/%s'%img},
              'quiz_info':simplejson.loads(d.quiz_info),
              #'slug':d.slug

          }
          context['dinamica'] = simplejson.dumps(dina,default=date_handler)
        else:
          dina = None

          


        userp = {'name':'Alberto','profile':'admin'}

        context['cur_page'] = {}
        context['user'] = userp
        context['pages'] = simplejson.dumps({})
        context['djangorows'] = {}
        

        response = render(request, self.template, context)
        return response

addDinamica = addDinamica.as_view()



class saveDin(View):

    template = 'dinamicasapp/adddinamica.html'

    def get(self, request):

        data = request.GET.copy()

        dpk = data.get('dpk',None)
        quiz_info = request.GET.getlist('quiz_info')
        
        if dpk:
          d = Dinamica.objects.get(pk=dpk)
        else:
          d = None

        f = FormCreator()
        lista = ['titulo','bkcolor','inicia','finaliza','bases','orden']
        forma = f.form_to_model(modelo=Dinamica,excludes=[],fields=lista)
        forma = forma(data,instance=d)
        #forma.quiz_info = simplejson.loads(quiz_info)
        po = []
        for x in quiz_info:
          x = simplejson.loads(x)
          po.append(x)

        if forma.is_valid():
          saved = forma.save()
          saved.quiz_info = simplejson.dumps(po)
          saved.save()

        else:
          assert False,forma.errors    

        response = {'dpk':saved.pk,'saved':'ok'}

        return JsonResponse(response)
        

saveDin = saveDin.as_view()




class addCat(View):

  def get(self,request):
    data = request.GET.copy()

    cpk = data.get('cpk','0')

    if cpk=='0':
      p = Promocat()
    else:
      p = Promocat.objects.get(pk=cpk)
    p.catname = data.get('name')
    p.catslug = slugify(data.get('name',''))
    p.save()
    response = {'pk':p.pk}
    return JsonResponse(response)


addCat = addCat.as_view()




class addSCat(View):

  def get(self,request):
    data = request.GET.copy()
    parentcat = data.get('parentcat',None)
    cpk = data.get('cpk','0')

    if cpk=='0':
      p = Promocat()
    else:
      p = Promocat.objects.get(pk=cpk)

    p.catname = data.get('name')
    p.catslug = slugify(data.get('name',''))
    p.parentcat = Promocat.objects.get(pk=parentcat)    
    p.save()

    response = {'pk':p.pk}
    return JsonResponse(response)


addSCat = addSCat.as_view()


class rmCat(View):

  def get(self,request):
    data = request.GET.copy()

    parentcat = data.get('parentcat',None)
    cpk = data.get('cpk','0')
    if cpk=='0':
      p = Promocat()
    else:
      p = Promocat.objects.get(pk=cpk)
    p.delete()

    response = {'pk':p.pk}
    return JsonResponse(response)


rmCat = rmCat.as_view()



class savePalabra(View):


  def get(self,request):
    response = {}
    data = request.GET.copy()
    promopk = data.get('promopk',None)
    pk = data.get('pk','0')
    if promopk:
      promo = Promocion.objects.get(pk=promopk)
      if pk=='0':
        preg = Dinpalabra()
      else: 
        preg = Dinpalabra.objects.get(pk=pk)

      preg.promopk = promo
      preg.description = data.get('description','null')
      preg.palabra = data.get('palabra','null')
      preg.save()
      response = {'pk':preg.pk}
    return JsonResponse(response)


savePalabra = savePalabra.as_view()




class addFotoPalabra(View):

  def post(self,request):
    data = request.POST.copy()
    cropimg = data.get('img')
    img,crop = cropimg.split(';base64,')
    imagen = crop.decode('base64')
    croped = Image.open(BytesIO(imagen))
    tempcrop = StringIO.StringIO()
    croped.save(tempcrop,format='PNG',dpi=(72,72))
    name_imagen = 'crop_%s.%s'%(data.get('pk'),croped.format.lower())        
    cropsafe = ContentFile(tempcrop.getvalue(),name_imagen)



    if data.get('pk',None):
      p = Dinpalabra.objects.get(pk=data.get('pk'))
      if data.get('ims','0')=='0':
        p.imagen_uno = cropsafe
      else:
        p.imagen_dos = cropsafe
            
      p.save()

      response = {'pk':'deleted'}
    else:
      response = {'pk':'no deleted'}


    return JsonResponse(response)


addFotoPalabra = addFotoPalabra.as_view()


class rmPalabra(View):

  def post(self,request):
    data = request.POST.copy()

    if data.get('pk',None):
      p = Dinpalabra.objects.get(pk=data.get('pk'))
      p.delete()
      response = {'pk':'deleted'}
    else:
      response = {'pk':'no deleted'}


    return JsonResponse(response)

rmPalabra = rmPalabra.as_view()




class saveMarcador(View):


  def get(self,request):
    response = {}
    data = request.GET.copy()
    promopk = data.get('promopk',None)
    pk = data.get('pk','0')
    if promopk:
      promo = Promocion.objects.get(pk=promopk)
      if pk=='0':
        preg = Dinfutbol()
      else: 
        preg = Dinfutbol.objects.get(pk=pk)

      preg.promopk = promo
      preg.marcador_uno = data.get('marcador_uno',None)
      preg.marcador_dos = data.get('marcador_dos',None) 
      preg.description = data.get('description','null')
      preg.respuesta = data.get('respuesta',False)
      print preg.respuesta
      preg.save()
      response = {'pk':preg.pk}
    return JsonResponse(response)


saveMarcador = saveMarcador.as_view()



class addFotoMarcador(View):

  def post(self,request):
    data = request.POST.copy()
    cropimg = data.get('img')
    img,crop = cropimg.split(';base64,')
    imagen = crop.decode('base64')
    croped = Image.open(BytesIO(imagen))
    tempcrop = StringIO.StringIO()
    croped.save(tempcrop,format='PNG',dpi=(72,72))
    name_imagen = 'crop_%s.%s'%(data.get('pk'),'png')        
    cropsafe = ContentFile(tempcrop.getvalue(),name_imagen)



    if data.get('pk',None):
      p = Dinfutbol.objects.get(pk=data.get('pk'))
      if data.get('ims','0')=='0':
        p.imagen_uno = cropsafe
      else:
        p.imagen_dos = cropsafe
            
      p.save()

      response = {'pk':'deleted'}
    else:
      response = {'pk':'no deleted'}


    return JsonResponse(response)


addFotoMarcador = addFotoMarcador.as_view()



class setWinner(View):

  def post(self,request):
    data = request.POST.copy()
    response = {}

    parti = Participacion.objects.get(pk=data.get('promopk',None))
    parti.ganadora = True
    parti.fecha_ganador = datetime.now()
    parti.usuario_asigna_ganador = request.user.pk
    parti.save()
    response = {'promo':parti.pk}

    return JsonResponse(response)

setWinner = setWinner.as_view()





class addVentaja(View,TimeMets):

  def get(self,request):
    data = request.GET.copy()
    params = {}
    params['inicio'] = datetime.strptime(data.get('inicio'), '%d/%m/%Y') # self.strfecha(data.get('inicio',None))
    params['fin'] =  datetime.strptime(data.get('fin'), '%d/%m/%Y') #  self.strfecha(data.get('fin',None))
    params['ventaja'] = data.get('ventaja',None)
    #params['terminos'] = data.get('vterminos','')



    ps = Pagesetts(**params)
    ps.save()
    response = {'pk':ps.pk}
    return JsonResponse(response)
addVentaja = addVentaja.as_view()


class rmVentaja(View):

  def get(self,request):
    data = request.GET.copy()
    pk = data.get('pk',None)
    if pk:
      p = Pagesetts.objects.get(pk=pk)
      p.delete()


    response = {'promo':0}

    return JsonResponse(response)

rmVentaja = rmVentaja.as_view()



class saveSwiper(View):

  def post(self,request):
    response = {}
    data = request.POST.copy()
    return JsonResponse(data)



  def get(self,request):
    response = {}
    data = request.GET.copy()
    pk = data.get('pk','0')

    if pk=='0':
      swipp = Swippregunta()
    else:
      swipp = Swippregunta.objects.get(pk=pk)
    swipp.promopk_id = data.get('promopk')
    swipp.pregunta = data.get('pregunta','Pregunta')
    swipp.save()
    response['pk']=swipp.pk
    return JsonResponse(response)


saveSwiper = saveSwiper.as_view()


class saveImSwiper(View):

  def post(self,request):
    response = {}
    data = request.POST.copy()
    cropimg = data.get('imagen')
    formats,crop = cropimg.split(';base64,')
    imagen = crop.decode('base64') 
    croped = Image.open(BytesIO(imagen))
    tempcrop = StringIO.StringIO()
    croped.save(tempcrop,format='PNG',dpi=(72,72))
    name_imagen = 'swiper_%s.png'%(data.get('pk'))        
    cropsafe = ContentFile(tempcrop.getvalue(),name_imagen)

    swpimg = Swipimages()
    swpimg.prgeuntapk_id=data.get('pk')
    swpimg.imagen = cropsafe
    swpimg.save()

    response['img']=swpimg.imagen.name
    response['imgpk']=swpimg.pk

    return JsonResponse(response)


  def get(self,request):

    response = {}
    data = request.GET.copy()

    sp = Swipimages.objects.get(pk=data.get('imgpk'))
    sp.sideimg = data.get('sideimg')

    sp.save()

    response['saved'] = sp.sideimg

    return JsonResponse(response)




saveImSwiper = saveImSwiper.as_view()



class rmImSwiper(View):

  def get(self,request):
    response = {}
    data = request.GET.copy()

    sp = Swipimages.objects.get(pk=data.get('imgpk'))
    try:
      os.remove(sp.imagen.path)
    except:
      pass
    sp.delete()

    return JsonResponse(response)

rmImSwiper = rmImSwiper.as_view()



class rmSwiper(View):

  def get(self,request):
    response = {}
    data = request.GET.copy()
    pk = data.get('pk','0')

    if pk=='0':
      swipp = Swippregunta()
    else:
      swipp = Swippregunta.objects.get(pk=pk)
      for x in swipp.swipimages_set.all():
        try:
          os.remove(x.imagen.path)
        except:
          pass
      swipp.delete()
    return JsonResponse(response)


rmSwiper = rmSwiper.as_view()




class saveDinTer(View):

  def get(self,request):
    response = {}
    data = request.GET.copy()

    if data.get('slug',None):
      dinter,fail = Dinamicaterminos.objects.get_or_create(dinamicaslug=data.get('slug'))
      dinter.terminos = data.get('terms')
      dinter.descp = data.get('descp')
      dinter.instructivo = data.get('instructivo')
      dinter.textoganadoresdinamica = data.get('textoganadoresdinamica','')
      dinter.save()
      response['pk']=dinter.pk
    return JsonResponse(response)


saveDinTer = saveDinTer.as_view()




@csrf_exempt
def saveTermstxt(request):
  response = {}
  data = request.POST.copy()
  if data.get('mensaje',None):
    
    term = Terminos.objects.all()
    term.delete()

    terminos_data = data.get('mensaje')
    terminos = Terminos(texto = terminos_data)
    terminos.texto_recogerprovincia = data.get('texto_recogerprovincia','')
    terminos.texto_recogercdmx = data.get('texto_recogercdmx','')
    terminos.texto_recogerterceros = data.get('texto_recogerterceros','')
    terminos.save()
    response['pk']=terminos.pk
  return JsonResponse(response)


