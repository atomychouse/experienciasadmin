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

from dinamicasapp.models import * 

#IMAGE LIBS
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.files import File

from base64 import b64decode
import StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile

class ImgProcess:

    def bancoimg(self,data):
        
        cropimg = data.get('cropimg',None)
        rowpk = data.get('rowpk',None)
        itmpk = data.get('itmpk',0)
        filename = data.get('filename',None)
        prev = data.get('prev',None)
        fullimg = data.get('fullimg',None)

        basepath = settings.BASE_DIR

        prevpath = '%s%s'%(basepath,prev)
        prevImg = open(prevpath,'rb')
        prevsafe = File(prevImg)

        fullpath = '%s%s'%(basepath,fullimg)
        fullImg = open(fullpath,'rb')
        fullsafe = File(fullImg)
        
        formats,crop = cropimg.split(';base64,')
        imagen = crop.decode('base64') 
        croped = Image.open(BytesIO(imagen))
        tempcrop = StringIO.StringIO()
        croped.save(tempcrop,format='PNG',dpi=(72,72))
        name_imagen = 'crop_%s.%s'%(itmpk,croped.format.lower())        
        cropsafe = ContentFile(tempcrop.getvalue(),name_imagen)
        assert False,cropsafe

        if not filename:
            filename = fullpath.split('/')[-1]


        if int(itmpk)>0:
            itm = Itmmodulo.objects.get(pk=itmpk)
        else:
            modulo = Modulo.objects.get(pk=rowpk)
            itm = Itmmodulo(modulopk=modulo)
            itm.save()
        tokill = itm.mediaitm_set.all()
        for x in tokill:
            try: 
                os.remove(x.mimage.path)
            except:
                pass
            x.delete()

        mediacrop = Mediaitm()
        mediacrop.typo ='img'
        mediacrop.itmpk = itm            
        mediacrop.mimage = cropsafe           
        mediacrop.save()

        mediaprev = Mediaitm()
        mediaprev.typo ='prev'
        mediaprev.itmpk = itm                       
        mediaprev.save()
        mediaprev.mimage.save(filename,prevsafe,save=True)

        mediafull = Mediaitm()
        mediafull.typo ='full'
        mediafull.itmpk = itm                     
        mediafull.save()
        mediafull.mimage.save(filename,fullsafe,save=True)  

        os.remove(prevpath)
        os.remove(fullpath)

        response = {'img':mediacrop.mimage.name,
                    'prev':mediaprev.mimage.name,
                    'full':mediafull.mimage.name,
                    'itm':itm.pk
                    }

        return response


    def header(self,data):
        itmpk = data.get('itmpk',0)
        rowpk = data.get('rowpk',None)
        filename = data.get('filename',None)
        cropimg = data.get('cropimg',None)
        formats,crop = cropimg.split(';base64,')
        prev = data.get('prev',None)
        fullimg = data.get('fullimg',None)

        basepath = settings.BASE_DIR

        prevpath = '%s%s'%(basepath,prev)
        fullpath = '%s%s'%(basepath,fullimg)
        os.remove(prevpath)
        os.remove(fullpath)


        imagen = crop.decode('base64') 
        croped = Image.open(BytesIO(imagen))
        tempcrop = StringIO.StringIO()
        croped.save(tempcrop,format='PNG',dpi=(72,72))
        name_imagen = 'crop_%s.%s'%(itmpk,croped.format.lower())
        
        cropsafe = ContentFile(tempcrop.getvalue(),name_imagen)



        if int(itmpk)>0:
            itm = Itmmodulo.objects.get(pk=itmpk)
        else:
            modulo = Modulo.objects.get(pk=rowpk)
            itm = Itmmodulo(modulopk=modulo)
            itm.save()
        
        tokill = itm.mediaitm_set.all()
        for x in tokill:
            os.remove(x.mimage.path)
            x.delete()

        mediacrop = Mediaitm()
        mediacrop.typo ='img'
        mediacrop.itmpk = itm            
        mediacrop.mimage = cropsafe           
        mediacrop.save()

        response = {'img':mediacrop.mimage.name,
                    'itm':itm.pk
                    }

        return response

    def gridlink(self,data):
        itmpk = data.get('itmpk',0)
        rowpk = data.get('rowpk',None)
        filename = data.get('filename',None)
        cropimg = data.get('cropimg',None)
        formats,crop = cropimg.split(';base64,')
        prev = data.get('prev',None)
        fullimg = data.get('fullimg',None)

        basepath = settings.BASE_DIR

        prevpath = '%s%s'%(basepath,prev)
        fullpath = '%s%s'%(basepath,fullimg)
        os.remove(prevpath)
        os.remove(fullpath)


        imagen = crop.decode('base64') 
        croped = Image.open(BytesIO(imagen))
        tempcrop = StringIO.StringIO()
        croped.save(tempcrop,format='PNG',dpi=(72,72))
        name_imagen = 'crop_%s.%s'%(itmpk,croped.format.lower())
        
        cropsafe = ContentFile(tempcrop.getvalue(),name_imagen)



        if int(itmpk)>0:
            itm = Itmmodulo.objects.get(pk=itmpk)
        else:
            modulo = Modulo.objects.get(pk=rowpk)
            itm = Itmmodulo(modulopk=modulo)
            itm.save()
        
        tokill = itm.mediaitm_set.all()
        for x in tokill:
            os.remove(x.mimage.path)
            x.delete()

        mediacrop = Mediaitm()
        mediacrop.typo ='img'
        mediacrop.itmpk = itm            
        mediacrop.mimage = cropsafe           
        mediacrop.save()

        response = {'img':mediacrop.mimage.name,
                    'itm':itm.pk
                    }

        return response


    def imgrebase(self,data):

        itmpk = data.get('itmpk',0)
        rowpk = data.get('rowpk',None)
        filename = data.get('filename',None)
        cropimg = data.get('cropimg',None)
        formats,crop = cropimg.split(';base64,')
        prev = data.get('prev',None)
        fullimg = data.get('fullimg',None)

        basepath = settings.BASE_DIR

        prevpath = '%s%s'%(basepath,prev)
        fullpath = '%s%s'%(basepath,fullimg)
        os.remove(prevpath)
        os.remove(fullpath)


        imagen = crop.decode('base64') 
        croped = Image.open(BytesIO(imagen))
        tempcrop = StringIO.StringIO()
        croped.save(tempcrop,format='PNG',dpi=(72,72))
        name_imagen = 'crop_%s.%s'%(itmpk,croped.format.lower())
        
        cropsafe = ContentFile(tempcrop.getvalue(),name_imagen)



        if int(itmpk)>0:
            itm = Itmmodulo.objects.get(pk=itmpk)
        else:
            modulo = Modulo.objects.get(pk=rowpk)
            itm = Itmmodulo(modulopk=modulo)
            itm.save()
        
        tokill = itm.mediaitm_set.all()
        for x in tokill:
            os.remove(x.mimage.path)
            x.delete()

        mediacrop = Mediaitm()
        mediacrop.typo ='img'
        mediacrop.itmpk = itm            
        mediacrop.mimage = cropsafe           
        mediacrop.save()

        response = {'img':mediacrop.mimage.name,
                    'itm':itm.pk
                    }

        return response


    def treseiscero(self,data):
        
        cropimg = data.get('cropimg',None)
        rowpk = data.get('rowpk',None)
        itmpk = data.get('itmpk',0)
        filename = data.get('filename',None)
        prev = data.get('prev',None)
        fullimg = data.get('fullimg',None)

        basepath = settings.BASE_DIR

        fullpath = '%s%s'%(basepath,fullimg)
        fullImg = open(fullpath,'rb')
        fullsafe = File(fullImg)
        


        if not filename:
            filename = fullpath.split('/')[-1]


        if int(itmpk)>0:
            itm = Itmmodulo.objects.get(pk=itmpk)
        else:
            modulo = Modulo.objects.get(pk=rowpk)
            itm = Itmmodulo(modulopk=modulo)
            itm.save()
        tokill = itm.mediaitm_set.all()
        for x in tokill:
            try: 
                os.remove(x.mimage.path)
            except:
                pass
            x.delete()


        mediafull = Mediaitm()
        mediafull.typo ='img'
        mediafull.itmpk = itm                     
        mediafull.save()
        mediafull.mimage.save(filename,fullsafe,save=True)  

        os.remove(fullpath)

        response = {'img':mediafull.mimage.name,                    
                    'itm':itm.pk
                    }

        return response


    def dinamica(self,data):

        dpk = data.get('dpk',0)
        cropimg = data.get('cropimg',None)
        formats,crop = cropimg.split(';base64,')

        basepath = settings.BASE_DIR
        imagen = crop.decode('base64') 
        croped = Image.open(BytesIO(imagen))
        tempcrop = StringIO.StringIO()
        croped.save(tempcrop,format='PNG',dpi=(72,72))
        name_imagen = 'crop_%s.%s'%(dpk,croped.format.lower())
        
        cropsafe = ContentFile(tempcrop.getvalue(),name_imagen)


        d = Dinamica.objects.get(pk=dpk)
        mm = d.mediadim_set.all()
        for x in mm:
            os.remove(x.myimg.path)
        mm.delete()

        mediacrop = Mediadim()

        mediacrop.dinamicapk = d            
        mediacrop.myimg = cropsafe           
        mediacrop.save()

        response = {'img':mediacrop.myimg.name,
                    'd':mediacrop.pk
                    }

        return response



    def dinamica_params(self,data):

        dpk = data.get('dpk',0)
        cropimg = data.get('cropimg',None)
        formats,crop = cropimg.split(';base64,')

        basepath = settings.BASE_DIR
        imagen = crop.decode('base64') 
        croped = Image.open(BytesIO(imagen))
        tempcrop = StringIO.StringIO()
        croped.save(tempcrop,format='PNG',dpi=(72,72))
        name_imagen = 'crop_%s.%s'%(dpk,croped.format.lower())
        
        cropsafe = ContentFile(tempcrop.getvalue(),name_imagen)


        d = Dinamica.objects.get(pk=dpk)
        mm = d.mediadim_set.all()
        for x in mm:
            os.remove(x.myimg.path)
        mm.delete()

        mediacrop = Mediadim()

        mediacrop.dinamicapk = d            
        mediacrop.myimg = cropsafe           
        mediacrop.save()

        response = {'img':mediacrop.myimg.name,
                    'd':mediacrop.pk
                    }

        return response



class ImagenP(View):

    def post(self,request):
        data = request.POST.copy()
        imgproc = ImgProcess()
        function_names = {
            'bancoimg':'bancoimg',
            'header':'header',
            'gridlink':'gridlink',
            'gridimg':'gridlink',
            'imgrebase':'imgrebase',
            'tresseiscero':'treseiscero',
            'ambientes':'treseiscero',
            'notas':'imgrebase',
            'imagenlateral':'imgrebase',
            'dinamica':'dinamica',
            'dinamica_params':'dinamica_params'
        }
        funcname = function_names[data['slug']]
        func = getattr(imgproc,funcname,None)
        plis = func(data)
        return JsonResponse(plis)

ImagenP = ImagenP.as_view()


class addModulo(View):

    def post(self,request):
        data = request.POST.copy()
        pagepk = int(data.get('pagepk','0'))
        rowpk = int(data.get('rowpk','0'))
        lista = ['mtitle','typ','slug','orden']

        if rowpk>0:
            md = Modulo.objects.get(pk=rowpk)
        else:
            md = Modulo()
        for x in lista:
            dato = data.get(x,None)
            if dato:
                md.__setattr__(x,dato)
        if pagepk>0:
            pg = Wpage.objects.get(pk=pagepk)                
            md.page = pg
        md.mtitle = data.get('mtitle','')
        
        md.save()
        response = {'rowpk':md.pk}
        return JsonResponse(response)
    def get(self, request):
        assert False,'morbius'

addModulo = addModulo.as_view()


class addCategoria(View):

    def post(self,request):
        data = request.POST.copy()
        catpk = int(data.get('catpk','0'))
        rowpk = int(data.get('rowpk','0'))
        parcatpk = int(data.get('parcatpk','0'))

        lista = ['catname','slug','orden']
        
        if catpk>0:
            cat = Categoria.objects.get(pk=catpk)
        else:
            cat = Categoria()
        for x in lista:
            dato = data.get(x,None)
            if dato:
                cat.__setattr__(x,dato)
        
        if rowpk>0:
            md = Modulo.objects.get(pk=rowpk)                
            cat.modulopk = md
        if parcatpk>0:
            pcat = Categoria.objects.get(pk=parcatpk)
            cat.parentcat = pcat

        cat.save()
        response = {'catpk':cat.pk}
        return JsonResponse(response)
    def get(self, request):
        assert False,'gorgeous'

addCategoria = addCategoria.as_view()



class addItm(View):

    def post(self,request):
        data = request.POST.copy()
        rowpk = int(data.get('rowpk','0'))
        itmpk = int(data.get('itmpk','0'))

        lista = ['titulo','descp','orden']
        if itmpk>0:
            itm = Itmmodulo.objects.get(pk=itmpk)
        else:
            itm = Itmmodulo()

        for x in lista:
            dato = data.get(x,None)
            if dato:
                itm.__setattr__(x,dato)
        
        if rowpk>0:
            md = Modulo.objects.get(pk=rowpk)                
            itm.modulopk = md

        itm.save()
 


        response = {'itmpk':itm.pk}
        return JsonResponse(response)

    
    def get(self, request):
        data = request.GET.copy()
        rowpk = int(data.get('rowpk','0'))
        itmpk = int(data.get('itmpk','0'))


        lista = ['titulo','descp','orden']
        if itmpk>0:
            itm = Itmmodulo.objects.get(pk=itmpk)
        else:
            itm = Itmmodulo()

        for x in lista:
            dato = data.get(x,None)
            if dato:
                itm.__setattr__(x,dato)
        
        if rowpk>0:
            md = Modulo.objects.get(pk=rowpk)                
            itm.modulopk = md

        itm.save()
        
        params = simplejson.loads(request.GET['params'])

        pas = Paramitm.objects.filter(itmpk=itm.pk,typo=params['type'])
        pas.delete()

        
        parametro = simplejson.dumps({data.get('clave','link'):params.get('value',None)})

        itmpar = {'itmpk':itm,'typo':params['type'],'params':parametro}
        pr = Paramitm(**itmpar)
        pr.save()



        response = {'itmpk':itm.pk}
        return JsonResponse(response)


addItm = addItm.as_view()




class addColor(View):
 
    def get(self, request):
        data = request.GET.copy()
        rowpk = int(data.get('rowpk','0'))
        itmpk = int(data.get('itmpk','0'))


        lista = ['titulo','descp','orden']
        if itmpk>0:
            itm = Itmmodulo.objects.get(pk=itmpk)
        else:
            itm = Itmmodulo()

        for x in lista:
            dato = data.get(x,None)
            if dato:
                itm.__setattr__(x,dato)
        
        if rowpk>0:
            md = Modulo.objects.get(pk=rowpk)                
            itm.modulopk = md

        itm.save()
        


        params = simplejson.loads(request.GET['params'])
        pas = Paramitm.objects.filter(itmpk=itm.pk,typo='color')
        pas.delete()
        parametro = simplejson.dumps(params)
        itmpar = {'itmpk':itm,'typo':'color','params':parametro}
        pr = Paramitm(**itmpar)
        pr.save()

        response = {'itmpk':itm.pk}
        return JsonResponse(response)


addColor = addColor.as_view()




class saveMyCats(View):

    def post(self,request):
        return JsonResponse({'saved':'ok'})
    
    def get(self, request):
        data = request.GET.copy()
        response = {}

        itmpk = data.get('itmpk',None)
        typo = 'mycats'
        mycats = request.GET.getlist('mycats')
        itm = Itmmodulo.objects.get(pk=itmpk)
        itmparams,faits = Paramitm.objects.get_or_create(typo=typo,itmpk=itm)
        itmparams.params = simplejson.dumps(mycats)
        itmparams.save()
        response['saved']={'pk':itmparams.pk,'itmpk':itmpk}

        return JsonResponse(response)

saveMyCats = saveMyCats.as_view()



class rmItm(View):

    def post(self,request):
        data = request.POST.copy()
        itmpk = int(data.get('itmpk','0'))
        if itmpk>0:
            itm = Itmmodulo.objects.get(pk=itmpk)
            for m in itm.mediaitm_set.all():
                m.delete()
                os.remove(m.mimage.path)
            itm.delete()

        response = {'itmpk':'deleted'}
        return JsonResponse(response)
    
    def get(self, request):
        assert False,'morbius'

rmItm = rmItm.as_view()


class rmModulo(View):

    def post(self,request):
        data = request.POST.copy()
        rowpk = int(data.get('rowpk','0'))
        if rowpk>0:
            itm = Modulo.objects.get(pk=rowpk)
            for itmmd in itm.itmmodulo_set.all():
                for m in itmmd.mediaitm_set.all():
                    m.delete()
                    os.remove(m.mimage.path)
                itmmd.delete()

            itm.delete()           
        response = {'itmpk':'deleted'}
        return JsonResponse(response)
    
    def get(self, request):
        assert False,'morbius'

rmModulo = rmModulo.as_view()


class rmCat(View):

    def post(self,request):
        data = request.POST.copy()
        catpk = int(data.get('catpk','0'))
        if catpk>0:
            itm = Categoria.objects.get(pk=catpk)
            itm.delete()           
        response = {'itmpk':'deleted'}
        return JsonResponse(response)
    
    def get(self, request):
        response = {'itmpk':'deleted'}
        return JsonResponse(response)

rmCat = rmCat.as_view()



class addFile(View):

    def post(self,request):
        data = request.POST.copy()
        itmpk = int(data.get('itmpk','0'))
        filename = data.get('filename')
        archivestr = data.get('archivestr','')
        titulo = data.get('titulo','ABCDEFGHIJKLMNÑOPQRSTVWXYZ123456789')
        rowpk = data.get('rowpk',0)

        formats, imgstr = archivestr.split(';base64,')
        filesafe = ContentFile(b64decode(imgstr),name=filename)

        if itmpk>0:
            itm = Itmmodulo.objects.get(pk=itmpk)
            itm.titulo = titulo
            itm.save()


            itmfiles = itm.fileitm_set.all().delete()
        else:
            
            itm = Itmmodulo(titulo=titulo,modulopk=Modulo.objects.get(pk=rowpk))
            itm.save()            


        itmparam = itm.paramitm_set.filter(typo='params').delete()
        params = simplejson.dumps({'link':filename.split('.')[0]})
        itmparam = Paramitm(typo='params',itmpk=itm,params=params)
        itmparam.save()


        fileitm = Fileitm(modulopk=itm)
        fileitm.myfile = filesafe
        fileitm.save()
        response = {'itmtitulo':itm.titulo,'itmpk':itm.pk,'fpk':fileitm.pk,'file':fileitm.myfile.name,'name':filename.split('.')[0]}
        return JsonResponse(response)
    
    def get(self, request):
        assert False,'morbius'

addFile = addFile.as_view()


class rmFile(View):

    def post(self,request):
        data = request.POST.copy()
        itmfile = int(data.get('itmfile','0'))
        if itmfile>0:
            itm = Fileitm.objects.get(pk=itmfile)            
            itm.delete()
        
        response = {'itmpk':'deleted'}
        return JsonResponse(response)
    
    def get(self, request):
        assert False,'morbius'

rmFile = rmFile.as_view()

class saveCfg(View):

    def post(self,request):
        data = request.POST.copy()
 
        response = data
        return JsonResponse(response)
    def get(self, request):
        data = request.GET.copy()
        rowpk = data['rowpk']
        m = Modulo.objects.get(pk=rowpk)
        cfg,fails = Settsmodulo.objects.get_or_create(modulopk=m)
        cfg.confg = data['cfg']
        cfg.save()
        response = {'cfg':cfg.pk}
        return JsonResponse(response)
saveCfg = saveCfg.as_view()

class saveColumna(View):

    def post(self,request):
        data = request.POST.copy()
 
        response = data
        return JsonResponse(response)
    def get(self, request):
        data = request.GET.copy()
        pagepk = data.get('pagepk',None)
        colname = data.get('colname',None)
        colorden = data['orden']
        colpk = data.get('colpk',0)

        if int(colpk)>0:
            col = Catpage.objects.get(pk=colpk)
        else:
            col = Catpage()

        if pagepk:
            pageown = Wpage.objects.get(pk=pagepk)
            col.pageown = pageown

        col.catname = colname
        if not colname:
            colname = 'col %s'%(colorden)
        col.catslug = slugify(colname)
        col.orden = colorden
        
        col.save()
        response = {'colpk':col.pk,'slug':col.catslug}
        return JsonResponse(response)
saveColumna = saveColumna.as_view()


class savePage(View):


    def get(self, request):
        response = {}
        data = request.GET.copy()
        pagepk = data.get('pagepk',0)
        parentpk = data.get('parentpk',None)
        pagename = data.get('pagename',None)
        pagecol = data.get('pagecol',None)
        pageishome = data.get('ishome',False)
        orden = data.get('orden',1)
        try:
            current_site = get_current_site(request)
        except:
            current_site = None

        if pagename:
            pageslug = slugify(pagename)
        else:
            pagename = 'section %s'%(orden)
            pageslug = slugify(pagename)

        if int(pagepk)>0:
            page = Wpage.objects.get(pk=pagepk)
        else:
            page = Wpage()

        if parentpk:
            parentpage = Wpage.objects.get(pk=parentpage)
            page.parentpage = parentpage

        if pagecol:
            pagecol = Catpage.objects.get(pk=pagecol)
            page.columna = pagecol
            page.parentpage = pagecol.pageown


        page.name = pagename
        page.slug = pageslug
        page.ishome = pageishome
        page.status = 'onl'
        page.orden = orden
        
        page.sitio = current_site
        page.save()


        if pagepk == 0:
            
            data_modulo = {
                    'page':page,
                    'typ':'rebase',
                    'slug':'header',
                    'mtitle':'CABECERA',
                    'orden':1
                    }
            m = Modulo(**data_modulo)
            m.save()


            data_itm = {
            'modulopk':m,
            'titulo':page.name,
            'orden':1
            }
            itm = Itmmodulo(**data_itm)
            itm.save()


        response['pagepk']=page.pk
        response['pageslug']=page.slug


        return JsonResponse(response)
savePage = savePage.as_view()


class rmPage(View):

    def get(self,request):
        data = request.GET.copy()
        pagepk = data.get('pagepk',None)
        if pagepk:
            itm = Wpage.objects.get(pk=pagepk)
            if itm.issystem==False:
                itm.delete()           
        response = {'itmpk':'deleted'}
        return JsonResponse(response)    
rmPage = rmPage.as_view()




class rmColumn(View):

    def get(self,request):
        data = request.GET.copy()
        pagepk = data.get('catpk',None)
        if pagepk:
            itm = Catpage.objects.get(pk=pagepk)
            itm.delete()           
        response = {'itmpk':'deleted'}
        return JsonResponse(response)
    
rmColumn = rmColumn.as_view()


class dropImage(View):
    def post(self,request):
        data = request.POST.copy()
        filex = request.FILES['filex']
        #assert False,
        extention = filex.name.split('.')[-1]

        basedir = '%s/static/temps'%(settings.BASE_DIR)
        webpath = '/static/temps'

        user = request.user
        filename = '%s/%s_%s_min.%s'%(basedir,'promo',data['pk'],extention)
        fullfile = '%s/%s_%s_%s'%(basedir,'promo',data['pk'],filex.name)
        torm = '%s/%s_%s_min.*'%(basedir,'promo',data['pk'])
        webfilename = '%s/%s_%s_min.%s'%(webpath,'promo',data['pk'],extention)
        webfull = '%s/%s_%s_%s'%(webpath,'promo',data['pk'],filex.name)

        typef = filex.name.split('.')[-1].upper()
        #assert False,typef
        os.system('rm %s'%(torm))
        tempfile = Image.open(filex)
        wi = tempfile.width
        hi = tempfile.height
        th = hi * 0.5 #200.0
        tw = (th/hi) * wi
        newsize = (int(tw),int(th))
        thimg = tempfile.resize(newsize,Image.ANTIALIAS)
        formato = filex.content_type.split('/')
        thimg.save(filename, format=formato[1],dpi=(72,72))

        tempfile.close()


        response = {'cropimg':webfilename,'fullimage':webfull}

        return JsonResponse(response)
dropImage = dropImage.as_view()

class dropImagelg(View):
    def post(self,request):
        data = request.POST.copy()
        filex = request.FILES['filex']
        #assert False,
        extention = filex.name.split('.')[-1]

        basedir = '%s/static/temps'%(settings.BASE_DIR)
        webpath = '/static/temps'

        user = request.user
        filename = '%s/%s_%s_lg.%s'%(basedir,'promo',data['pk'],extention)
        torm = '%s/%s_%s_lg.*'%(basedir,'promo',data['pk'])
        fullfile = '%s/%s_%s_%s'%(basedir,'promo',data['pk'],filex.name)

        os.system('rm %s'%(torm))

        webfilename = '%s/%s_%s_lg.%s'%(webpath,'promo',data['pk'],extention)
        webfull = '%s/%s_%s_%s'%(webpath,'promo',data['pk'],filex.name)

        typef = filex.name.split('.')[-1].upper()
        #assert False,typef

        tempfile = Image.open(filex)
        wi = tempfile.width
        hi = tempfile.height
        th = hi * 0.5 #200.0
        tw = (th/hi) * wi
        newsize = (int(tw),int(th))
        thimg = tempfile.resize(newsize,Image.ANTIALIAS)
        formato = filex.content_type.split('/')
        thimg.save(filename, format=formato[1],dpi=(72,72))

        tempfile.close()


        response = {'cropimg':webfilename,'fullimage':webfull}

        return JsonResponse(response)
dropImagelg = dropImagelg.as_view()


class addParam(View):

    def get(self,request):
        data = request.GET.copy()
        response = {}
        itmpk = data.get('itmpk',0)

        if int(itmpk)==0:
            return JsonResponse({'no itm':'no'})

        itm = Itmmodulo.objects.get(pk=itmpk)
        params = data['nota']
        typo = 'markas'

        prm = Paramitm(itmpk=itm)
        prm.typo = 'markas'
        prm.params = params

        prm.save()

        response['prmpk']=prm.pk

        return JsonResponse(response)

addParam = addParam.as_view()



class rmParam(View):

    def get(self,request):
        data = request.GET.copy()
        response = {}


        p = Paramitm.objects.get(pk=data['prmpk']).delete()
        response['prmpk']='deleted %s'%(data['prmpk'])

        return JsonResponse(response)

rmParam = rmParam.as_view()


class upParam(View):

    def get(self,request):
        data = request.GET.copy()
        response = {}


        p = Paramitm.objects.get(pk=data['prmpk'])
        params = simplejson.loads(p.params)
        params['tooltip'] = data['tooltip']
        params['orden'] = data['orden']
        params = simplejson.dumps(params)
        p.params = params
        p.save()

        response['prmpk']='saved %s'%(data['prmpk'])

        return JsonResponse(response)

upParam = upParam.as_view()




class Reorder(View):

    def get(self,request):
        data = request.GET.copy()
        listado = data.getlist('listado')
        for l in listado:
            param = simplejson.loads(l)
            try:
                m = Modulo.objects.get(pk=param['pk'])
                m.orden = param['orden']
                m.save()
            except:
                pass

        response = {}



        response['prmpk']='saved'

        return JsonResponse(response)

Reorder = Reorder.as_view()




class AddImage(View):

    def post(self,request):

        data = request.POST.copy()
        itmpk = data.get('pk',None)
        typo = data.get('typo',None)
        response = {}
                
        archivo = request.FILES['filex']
        p = Promocion.objects.get(pk=itmpk)
        p.mediapromo_set.filter(tipoimg=typo).delete()
        media,nomedia = Mediapromo.objects.get_or_create(promo=p,tipoimg=typo)
        media.imagen=archivo
        media.save()
        response['imagen']=media.imagen.name
        return JsonResponse(response)
AddImage = AddImage.as_view()


class AddImageG(View):

    def post(self,request):
        data = request.POST.copy()
        itmpk = data.get('pk',None)
        typo = data.get('typo',None)
        response = {}
        archivo = request.FILES['filex']
        p = Promocion.objects.get(pk=itmpk)
        media = Mediapromo(promo=p,tipoimg=typo)
        media.imagen=archivo
        media.save()
        response['ipk']=media.pk
        response['imagen']=media.imagen.name;

        return JsonResponse(response)
    

AddImageG = AddImageG.as_view()


class rmGaleria(View):

    def get(self,request):
        response = {}
        pk = request.GET.get('gpk',None)
        m = Mediapromo.objects.get(pk=pk)
        m.delete()
        response['rm']='ok'
        return JsonResponse(response)
    

rmGaleria = rmGaleria.as_view()