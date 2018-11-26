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
from motorapp.models import * 
from dinamicasapp.models import * 
from mobapp.views import TimeMets
import xlsxwriter
from .sopa_de_letras import * 
import StringIO
import pytz

class Index(View):

    template = 'frontapp/index.html'

    def get(self, request,pks=None):
        context = {}
        search = {}
        userp = {'name':'Alberto','profile':'admin'}
        context['user'] = userp
        context['promocat'] = Promocat.objects.filter(parentcat=None)  
        mxtz = pytz.timezone('America/Mexico_City')
        hoy = datetime.datetime.now(mxtz)
        nextw = datetime.datetime.now(mxtz) + datetime.timedelta(days=7)
        nextq = datetime.datetime.now(mxtz) + datetime.timedelta(days=15)
        redsfecha = hoy - datetime.timedelta(days=1)
        reds = Promocion.objects.filter(Q(status='finalizado') | Q(vigencia__lte=redsfecha))

        proximamentes = Promocion.objects.filter(Q(status='proximamente'))
        activas = Promocion.objects.filter(Q(vigencia__gte=redsfecha))
        
        context['reds'] = reds
        context['proximamentes'] = proximamentes
        context['activas'] = activas
        context['dinter'] = Dinamicaterminos.objects.all()
        context['feriados']  = 'no'

        response = render(request, self.template, context)
        return response

Index = Index.as_view()





class calendarioDin(View):

    template = 'frontapp/calendario.html'

    def get(self, request,pks=None):
        context = {}
        search = {}

        grafica_meses = {}
        listado_meses = {}

        mxtz = pytz.timezone('America/Mexico_City')
        hoymas = datetime.datetime.now(mxtz) - datetime.timedelta(days=30)
        promos_today = Promocion.objects.filter(fecha_publicacion__gte=hoymas).order_by('fecha_publicacion').first()
        lastpromo = Promocion.objects.all().order_by('-vigencia').first()
        step = datetime.timedelta(1*365/12)

        inicio = promos_today.fecha_publicacion - datetime.timedelta(days=30)
        if lastpromo.vigencia:

            final = lastpromo.vigencia + datetime.timedelta(days=30)
        else:
            final = datetime.datetime.now(mxtz) + datetime.timedelta(days=10)
            final = final.date()

        while inicio <= final:
            
            promos = Promocion.objects.filter(fecha_publicacion__month=inicio.month,fecha_publicacion__year=inicio.year)
            finalizan = Promocion.objects.filter(vigencia__month=inicio.month,vigencia__year=inicio.year)
            online = Promocion.objects.filter(status='publish',vigencia__gte=inicio-datetime.timedelta(days=30))
            grafica_meses[inicio.month] = {'sepublican':promos.count(),'finalizan':finalizan.count(),'online':online.count()} 
            listado_meses[inicio.month] = {'sepublican':promos,'finalizan':finalizan,'online':online} 


            inicio += step


        feriados = []
        calendariotelcel = Calendariotelcel.objects.dates('fecha_completa','year')
        meses_arr = []
        for x in calendariotelcel:
            meses = Calendariotelcel.objects.dates('fecha_completa','month').filter(fecha_completa__year=x.year)
            params = []
            for m in meses:
                
                dias = Calendariotelcel.objects.dates('fecha_completa','day').filter(fecha_completa__month=m.month)
                fordias = []
                for d in dias:
                    fordias.append(d.day)
                    
                params.append({'name':m.month,'digit':m.month,'dias':fordias})

            anyo = {'year':x.year,'params':params}
            feriados.append(anyo)

        


        context['grafica_meses'] = grafica_meses
        context['listado_meses'] = listado_meses
        context['activas'] = Promocion.objects.filter(status='publish').order_by('fecha_evento')
        context['proxi'] = Promocion.objects.filter(status='proximamente').order_by('fecha_evento')
        context['feriados'] = simplejson.dumps(feriados)
        #context['promos'] = promos



        response = render(request, self.template, context)
        return response

calendarioDin = calendarioDin.as_view()



class Detail(View):

    template = 'frontapp/detail.html'

    def fecha_to_str(self,fecha):
        return datetime.datetime.strftime(fecha, '%b. %d | %Y')

    def get(self, request,pks=None):
        context = {}

        search = {}

        promo = Promocion.objects.get(pk=pks)

        if request.user.is_active:
            participo = request.user.participacion_set.all()
        else:
            participo = None


        context['pks'] = pks
        context['promo'] = promo
        context['participo'] = participo
        


        response = render(request, self.template, context)
        return response

Detail = Detail.as_view()


class Signin(View):

    template = 'frontapp/login.html'

    def get(self, request,secty=None,lugy=None,columna=None):
        
        logout(request)

        data = request.GET.copy()
        context = {}
        response = render(request, self.template, context)
        return response
Signin = Signin.as_view()



class Downloads(View):

    def get(self,request):
        filekey = request.GET.get('f',None)

        filename = '%s/%s'%(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),filekey)
        mm = mimetypes.guess_extension(filename)
        mtype = mimetypes.guess_type(filename)
        downloadame,extension = os.path.splitext(filename)
        datename = '%s'%datetime.datetime.now()
        nuname = '%s%s'%(slugify(datename),extension)
        f = open(filename)
        response = HttpResponse(f,content_type=mtype[0])

        dname_list = downloadame.split('/')
        dname = dname_list[len(dname_list)-1]

        response['Content-Disposition'] = 'attachment; filename="%s%s"'%(dname,extension)
        return response
Downloads = Downloads.as_view()



class Sin(View):

    def post(self,request):
        data = request.POST.copy()
        user = authenticate(username=data['usuarius'], password=data['passo'])
        response = {}
        
        try:
            group = user.groups.values()[0]['name']
        except:
            group = 'basic'

        if user is not None:
            login(request, user)
            response['saved'] = 'ok'
            response['datos'] = {'msg':u'guardao con éxito','liga':'/admin/'}
            response['callback'] = 'reg_success'
        else:
            response['msg'] = 'la información no es correcta, verifique por favor'
            response['errors'] = 'Usuario y/o contraseña incorrecta'

        return HttpResponse(simplejson.dumps(response))


Sin = Sin.as_view()



class Register(View):
    """Delete company."""
    template = 'mainapp/register.html'
    f = FormCreator()
    forma = f.form_to_model(modelo=User,fields=['username','password','email','is_active','is_staff'])



    def post(self,request):
        context = {}
        data = request.POST.copy()
 
        data['username'] = slugify(data.get('username'))
        passs = User.objects.make_random_password()
        data['password'] =  make_password(passs)
        data['is_active']=True
        data['is_staff']=True


        self.forma.base_fields['email'].required = True

        forma = self.forma(data)



        if forma.is_valid():
            saved = forma.save()
            context['ok'] = saved.id
            u = User.objects.get(pk=saved.id)
            user = authenticate(username=u.username, password=passs)            
            login(request,user)
        else:
            context['errors'] = forma.errors

        context = simplejson.dumps(context)
        return HttpResponse(context)

Register = Register.as_view()


class Participa(View):
    """Delete company."""
    template = 'mainapp/register.html'
    f = FormCreator()



    def get(self,request):
        context = {}
        data = request.GET.copy()
 
        uss = request.user
        promo = Promocion.objects.get(pk=data.get('promo'))
        parti,pl = Participacion.objects.get_or_create(promopk=promo,usuario=uss)
        parti.tiempo = '%s:%s'%(data.get('mins','0'),data.get('segs'))
        parti.save()

        respuestas = request.POST.getlist('pregunta')
        
        parti.resparticipacion_set.all().delete()
        correctas = 0

        for r in respuestas:
            
            anser = 'answer_%s'%(r)
            respues = Respuesta.objects.get(pk=data.get(anser))
            if respues.cor=='True':
                correctas = correctas + 1
            rx = Resparticipacion()
            rx.parti = parti
            rx.pregunta = r
            rx.respuesta = data.get(anser)
            rx.save()


        parti.nivelanswer = correctas
        parti.save()

        response = {'pk':'newpk'}
        return JsonResponse(response)
Participa = Participa.as_view()


class indexCategoria(View):

    def get(self,request):
        data = request.GET.copy()
        context = {}
        template = 'frontapp/categorias.html'
        promocat = Promocat.objects.filter(parentcat=None)

        context['promocat'] = promocat

        response = render(request,template, context)
        return response
indexCategoria = indexCategoria.as_view()


class Resultado(View,TimeMets):

    template = 'frontapp/resultados.html'

    def get(self, request,pks=None):



        context = {}
        search = {}
        promo = Promocion.objects.get(pk=pks)
        

        #parti = promo.participacion_set.all().order_by('-nivelanswer')
        parti = Participacion.objects.filter(promopk=promo,final__isnull=False).order_by('-nivelanswer','tiempo')[:200]

 
        
        filepad = '%s/frontapp/listados/promo_%s.xlsx' %(settings.BASE_DIR,pks)
        workbook = xlsxwriter.Workbook(filepad)
        worksheet = workbook.add_worksheet()
        worksheet.write('A1','%s %s'%(promo.linea_uno,promo.linea_dos))
        worksheet.write('A2','%s %s'%('',self.fecha_to_str(promo.fecha_evento,formato='%d de %m de %Y') ))
        #worksheet.write('A2','%s'%(

        worksheet.write('A5','Nombre')        
        worksheet.write('B5',u'Móvil')        
        worksheet.write('C5',u'Región')
        worksheet.write('D5','Correo')        
        worksheet.write('E5','Ventaja')        
        worksheet.write('F5','Aciertos')        
        worksheet.write('G5','Tiempo')        
        worksheet.write('H5',u'Inició')        
        worksheet.write('I5',u'Finalizó')        


        row = 5
        col = 0
        for p in parti:
            servicios = p.servicios_usuario()
            if p.tiempoJuega()!='no termino':
                tiempojuego = p.tiempoJuega() * 1000

            else:
                tiempojuego = p.tiempoJuega()
            
            try:
                servicios = servicios.replace('None,','')
                servicios = servicios.replace('None','')
            except:
                pass
                
            worksheet.write(row,0,p.usuario.profileuser_set.all().first().nombre_usuario)
            worksheet.write(row,1,p.usuario.profileuser_set.all().first().msisdn)
            worksheet.write(row,2,p.usuario.profileuser_set.all().first().region)
            worksheet.write(row,3,p.usuario.email)    
            worksheet.write(row,4,servicios)    
            worksheet.write(row,5,p.nivelanswer)    
            worksheet.write(row,6,p.tiempo)    
            worksheet.write(row,7,p.finicio())    
            worksheet.write(row,8,p.ffinal())    
            row += 1
        workbook.close()
        

        context['parti'] = parti
        context['promopk'] = pks
        context['promo'] = promo
        context['promocat'] = Promocat.objects.filter(parentcat=None)

        response = render(request, self.template, context)
        return response
Resultado = Resultado.as_view()



class Exfront(View):

    template = 'frontapp/ejemplosfront.html'

    def fecha_to_str(self,fecha):
        return datetime.datetime.strftime(fecha, '%b. %d | %Y')

    def get(self, request,pks=None):
    
        context = {}

        search = {}

        curr_page = Wpage.objects.filter(**search).first()
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

        prms = Promocion.objects.all()

        promos = [ {'pk':p.pk,
                    'titulo':p.titulo,
                    'linea_uno':p.linea_uno,
                    'linea_dos':p.linea_dos,
                    'header_final':p.header_final,
                    'linea_tres':p.linea_tres,                    
                    'vigencia':self.fecha_to_str(p.vigencia),
                    'color':p.color,
                    'dinamica':p.dinamica,
                    'media':{'firstimg':p.img,'imglg':p.imglg},
                    'status':p.status,
                    'likes':p.delikes_set.all().count(),
                    'bases':p.bases,
                    'terms':p.terms,
                    'segmentos':p.segs(),
                    'categorias':p.cats(),
                    'texto_alterno':p.texto_alterno,
                    'shares':p.shares,
                    'destacado':p.destacado,
                    'dins':p.dinsList(),
                    'orden':p.orden
                   } for p in prms]
        




        context['cur_page'] = curr_page
        context['user'] = userp
        context['pages'] = simplejson.dumps(pages)
        context['promos'] = simplejson.dumps(promos)
        context['promocat'] = Promocat.objects.filter(parentcat=None)        
        


        response = render(request, self.template, context)
        return response
Exfront = Exfront.as_view()


class allPromos(View,TimeMets):



    def get(self,request):
        data = request.GET.copy()        
        search = {}
        host = request.get_host()



        pek = data.get('pk',None)
        if pek:
            p = Promocion.objects.get(pk=pek)

            promo = {'pk':p.pk,
                    'titulo':p.titulo,
                    'linea_uno':p.linea_uno,
                    'linea_dos':p.linea_dos,
                    'header_final':p.header_final,
                    'vigencia':self.fecha_to_str(p.vigencia,formato='%d/%m/%Y'),
                    'vigencia_txt':self.fecha_to_str(p.vigencia),
                    'fecha_evento':self.fecha_to_str(p.fecha_evento,formato='%d/%m/%Y'),
                    'fecha_publicacion':self.fecha_to_str(p.fecha_publicacion,formato='%d/%m/%Y'),
                    'color':p.color,
                    'slug_titulo':p.slug_titulo,
                    'dinamica':p.dinamica,
                    'media':{'firstimg':p.img,'imglg':p.imglg},
                    'status':p.status,
                    'likes':p.delikes_set.all().count(),
                    'bases':p.bases,
                    'terms':p.terms,
                    'ciudad':p.ciudad,
                    'lugar':p.lugar,
                    'segmentos':p.segs(),
                    'categorias':p.cats(),
                    'texto_alterno':p.texto_alterno,
                    'participantes':p.participacion_set.all().count(),
                    'shares':p.shares,
                    'destacado':p.destacado,
                    'dins':p.dinsList(),
                    'imagenfinal':p.finalimg(host),
                    'minfinal':p.finalimg_min(host),
                    'galeria':p.galeria(host),
                    'matrix':p.tablero(),
                    'premioterms':p.premioterms,
                    'numero_ganadores':p.numero_ganadores,
                    'premio_frase':p.premio_frase
                   }

            return JsonResponse({'promocion':promo})
        else:
            prms = Promocion.objects.all().order_by('-destacado','-vigencia')
        
        promos = [ {'pk':p.pk,
                    'titulo':p.titulo,
                    'linea_uno':p.linea_uno,
                    'linea_dos':p.linea_dos,
                    'header_final':p.header_final,
                    'vigencia':self.fecha_to_str(p.vigencia,formato='%d/%m/%Y'),
                    'vigencia_txt':self.fecha_to_str(p.vigencia),
                    'fecha_evento':self.fecha_to_str(p.fecha_evento,formato='%d/%m/%Y'),
                    'fecha_publicacion':self.fecha_to_str(p.fecha_publicacion,formato='%d/%m/%Y'),
                    'color':p.color,
                    'dinamica':p.dinamica,
                    'media':{'firstimg':p.img,'imglg':p.imglg},
                    'status':p.estatus_admin(),
                    'likes':p.delikes_set.all().count(),
                    'bases':p.bases,
                    'terms':p.terms,
                    'ciudad':p.ciudad,
                    'lugar':p.lugar,
                    'segmentos':p.segs(),
                    'categorias':p.cats(),
                    'texto_alterno':p.texto_alterno,
                    'participantes':p.participacion_set.all().count(),
                    'shares':p.shares,
                    'destacado':p.destacado,
                    'dins':p.dinsList(),
                    'imagenfinal':p.finalimg(host),
                    'minfinal':p.finalimg_min(host),
                    'galeria':p.galeria(host),
                    'matrix':p.tablero(),
                    'premioterms':p.premioterms,
                    'orden':p.orden
                   } for p in prms]
        

        pagessetts = Pagesetts.objects.all().order_by('-inicio')
        ventajas = []
        for p in pagessetts:
            inicio = self.fecha_to_str(p.inicio)
            fin = self.fecha_to_str(p.fin)
            ventaja = p.ventaja
            pk = p.pk
            ven = {'ventaja':ventaja,'inicio':inicio,'fin':fin,'pk':pk}
            ventajas.append(ven)



        try: 
            terminostemplate = Terminos.objects.all().first()
            terminos = terminostemplate.texto
            texto_recogerprovincia = terminostemplate.texto_recogerprovincia
            texto_recogercdmx = terminostemplate.texto_recogercdmx
            texto_recogerterceros = terminostemplate.texto_recogerterceros
        except: 
            terminos = ''
            texto_recogerprovincia = ''
            texto_recogercdmx = ''
            texto_recogerterceros = ''

        promos = {'dinamicas':promos,'totales':len(promos),'ventajas':ventajas,
                  'terminos':terminos,
                  'texto_recogerprovincia':texto_recogerprovincia,
                  'texto_recogercdmx':texto_recogercdmx,
                  'texto_recogerterceros':texto_recogerterceros
                  }

        return JsonResponse(promos)
allPromos = allPromos.as_view()



class createSopa(View):
    def get(self,request):
        data = request.GET.copy()
        palabras = request.GET.getlist('palabras')
        promopk = data.get('promopk',None)
        matrix,posiciones = autonuevo(palabras=palabras)
        response = {'matrix':matrix,'pos':posiciones,'promo':promopk}
        p = Promocion.objects.get(pk=promopk)
        matrix = simplejson.dumps(matrix)
        posiciones = simplejson.dumps(posiciones)
        t,failt = Tablerosopa.objects.get_or_create(promopk=p)
        t.matrix=matrix
        t.posiciones=posiciones
        t.save()
        return JsonResponse(response,safe=False)


createSopa = createSopa.as_view()



class rmParti(View):
    def get(self,request,upk=None,dpk=None):
        response = {'eliminado':0}
        p = Participacion.objects.get(promopk_id=dpk,usuario_id=upk)
        p.delete()
        response['eliminado']=1
        return JsonResponse(response,safe=False)


rmParti = rmParti.as_view()



class addFeriado(View):

    template = 'frontapp/index.html'

    def post(self, request,pks=None):
        context = {}
        data = request.POST.copy()
        context = data
        fecha = datetime.datetime.strptime(data['diaferiado'],'%d/%m/%Y')
        cal,fail = Calendariotelcel.objects.get_or_create(fecha_completa=fecha,mes=fecha.month)
        cal.save()

        response = JsonResponse({'fecha':cal.fecha_completa,'dia':fecha.day,'mes':fecha.month,'year':fecha.year})
        return response

addFeriado = addFeriado.as_view()


class rmFeriado(View):


    def get(self, request,pks=None):
        context = {}
        data = request.GET.copy()

        context = data
        fecha = datetime.datetime.strptime(data['fecha'],'%d/%m/%Y')
        
        cal = Calendariotelcel.objects.filter(fecha_completa=fecha,mes=fecha.month)
        cal.delete()

        response = JsonResponse({'deleted':'ok'})
        return response

rmFeriado = rmFeriado.as_view()
