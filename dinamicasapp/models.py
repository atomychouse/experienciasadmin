# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User,Group
import simplejson
from django.db.models import Count
import os
import datetime
import pytz



class TimeMets():

    def fecha_to_str(self,fecha,formato='%b. %d | %Y'):
        tmz = pytz.timezone('America/Mexico_City')
        fecha = fecha.astimezone(tmz)
        try:
            return datetime.datetime.strftime(fecha,formato)
        except:
            return None
    def fecha_timestamp(self,fecha):
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


class Profileuser(models.Model):
    usuariopk = models.ForeignKey(User)
    nombre_usuario = models.CharField(max_length=200,blank=True,null=True)
    servicios = models.CharField(max_length=500,blank=True,null=True)
    date_reg = models.DateTimeField(auto_now_add=True)
    imagen = models.ImageField(upload_to='static/media/avatar/',blank=True,null=True)


class Pagesetts(models.Model):
    ventaja = models.CharField(max_length=100)
    inicio = models.DateField()
    terminos = models.TextField(blank=True,null=True)
    fin = models.DateField()

class Promocion(models.Model):
    titulo = models.TextField(blank=True,null=True)
    linea_uno = models.CharField(max_length=200, blank=True,null=True)
    linea_dos = models.CharField(max_length=200,blank=True,null=True)
    vigencia = models.DateField(blank=True,null=True)
    fecha_publicacion = models.DateField(blank=True,null=True)
    fecha_evento = models.DateField(blank=True,null=True)
    ciudad = models.CharField(max_length=200,blank=True,null=True)
    lugar = models.TextField(blank=True,null=True)
    status = models.CharField(max_length=50,default='working')
    orden = models.IntegerField(default=5,blank=True,null=True)
    dinamica = models.CharField(max_length=20,default='trivia',blank=True,null=True)
    color = models.CharField(max_length=50)
    shares = models.IntegerField(default=1)
    likes = models.IntegerField(default=1)
    img = models.CharField(max_length=500,blank=True,null=True)
    imglg = models.CharField(max_length=500,blank=True,null=True)
    bases = models.TextField(blank=True,null=True)
    terms = models.TextField(blank=True,null=True)
    segmentos = models.CharField(max_length=255,blank=True,null=True)
    categorias = models.CharField(max_length=255,blank=True,null=True)
    destacado = models.BooleanField(default=False)
    texto_alterno = models.TextField(blank=True,null=True)
    header_final = models.CharField(max_length=200,blank=True,null=True)
    premioterms = models.TextField(blank=True,null=True)
    reporte_enviado = models.IntegerField(blank=True,null=True)

    def yo_like(self,upk):
        if upk:
            if self.delikes_set.filter(userpk_id=upk):
                ya = 1
            else:
                ya = 0
        else:
            ya = 0

        return ya


    def yaparticipo(self,upk):
        if upk:
            p = self.participacion_set.filter(usuario_id=upk,final__isnull=False)
            if p:
                return True

            else:
                return False
        else:
            return False

    def activaono(self):
        date_format = "%m/%d/%Y"
        a = self.vigencia
        b = datetime.date.today()
        if (a-b).days>0:
            si = 1
        else:
            si = 0
        return  si

    def cats(self):
        if self.categorias:
            return simplejson.loads(self.categorias)
        else:
            return '[]'


    def segs(self):
        if self.segmentos:
            return simplejson.loads(self.segmentos)
        else:
            return '[]'



    def swiper(self):

        dinsa = [{
                 'promopk':self.pk, 
                 'pk':preg.pk,
                 'imgs':[ {'img':im.imagen.name,
                           'imgpk':im.pk,
                           'sideimg':im.sideimg
                            } for im in  preg.swipimages_set.all()],
                 'pregunta':preg.pregunta }
                        for preg in self.swippregunta_set.all()   ]
        return dinsa


    def front_swiper(self):

        dinsa = [{
                 'promopk':self.pk, 
                 'pk':preg.pk,
                 'imgs':[ {'img':im.imagen.name,
                           'imgpk':im.pk
                            } for im in  preg.swipimages_set.all()],
                 'pregunta':preg.pregunta }
                        for preg in self.swippregunta_set.all()   ]
        return dinsa



    def trivia(self):

        dinsa = [{'pk':preg.pk,
                             'indice':'',
                             'img':'/%s'%preg.imagen.name,
                             'pregunta':preg.pregunta,
                             'options':[{
                                          'rpk':res.pk,
                                          'indice':res.indice,
                                          'texto':res.resp ,
                                          'cor':res.cor,
                                            } 
                                    for res in preg.respuesta_set.all()] } for preg in self.pregunta_set.all().order_by('id')]
        return dinsa


    def palabras(self):
        dinsa = [{
                    'pk':x.pk,
                    'img':[x.imagen_uno.name,x.imagen_dos.name],
                    'description':x.description, 
                    'palabra':x.palabra}
                     for x in self.dinpalabra_set.all()]
        return dinsa



    def front_trivia(self):

        dinsa = [{'pk':preg.pk,
                             'indice':'',
                             'img':'https://admin.experienciastelcel.com/%s'%preg.imagen.name,
                             'pregunta':preg.pregunta,
                             'options':[{
                                          'rpk':res.pk,
					  'indice':res.indice,
                                          'texto':res.resp ,
                                          'cor':'',
                                            } 
                                    for res in preg.respuesta_set.all()] } for preg in self.pregunta_set.all().order_by('id')]
        return dinsa


    def sopa(self):
        dinsa = [{
                    'pk':x.pk,
                    'palabra':x.palabra}
                     for x in self.dinpalabra_set.all()]
        return dinsa

    def marcador_futbol(self):
        dinsa = [{
                    'pk':x.pk,
                    'imgs':[
                    {'img':x.imagen_uno.name,'marcador':x.marcador_uno},
                    {'img':x.imagen_dos.name,'marcador':x.marcador_dos},
                    ],
                    'description':x.description,
                    'respuesta':x.respuesta 
                    }
                     for x in self.dinfutbol_set.all()]

        return dinsa


    def front_sopa(self):
        dinsa = [{
                    'pk':x.pk,
                    'palabra':x.palabra}
                     for x in self.dinpalabra_set.all()]

        dins = self.tablerosopa_set.all().first()
        if dins:
            matrix = simplejson.loads(dins.lamatriz())
            
            poss = simplejson.loads(dins.posiciones)
            palabras = [ {'palabra':x.palabra} for x in self.dinpalabra_set.all()]
            dinsa = {'tablero':matrix,'lista':poss,'palabras':palabras}
        else:
            dinsa = None
        return dinsa

    def front_marcador_futbol(self):
        dinsa = [{
                    'pk':x.pk,
                    'imgs':[
                    {'img':'https://admin.experienciastelcel.com/%s'%(x.imagen_uno.name),'marcador':x.marcador_uno},
                    {'img':'https://admin.experienciastelcel.com/%s'%(x.imagen_dos.name),'marcador':x.marcador_dos},
                    ],
                    'description':x.description, 
                    }
                     for x in self.dinfutbol_set.all()]

        return dinsa



    def tablero(self):
        lista = {}
        tablero = self.tablerosopa_set.all().first()
        if tablero:
            lista = simplejson.loads(tablero.matrix)
        return lista


    def puzzle(self):
        lista = {}
        puzz = self.mediapromo_set.filter(tipoimg='puzzle')
        if puzz:
            lista = [{'puzzle':x.imagen.name} for x in puzz]
        else:
            lista = []

        return lista


    def front_puzzle(self):
        lista = {}
        puzz = self.mediapromo_set.filter(tipoimg='puzzle')
        if puzz:
            lista = [{'puzzle':x.imagen.name} for x in puzz]
        else:
            lista = []

        return lista        



    def dinsList(self):
        typo = self.dinamica
        classe = self
        func = getattr(classe,typo,None)
        if func:
            lista = func()
        else:
            lista = [] 
        return lista



    def frontList(self):
        typo = 'front_%s'%(self.dinamica)
        classe = self
        func = getattr(classe,typo,None)
        if func:
            lista = func()
        else:
            lista = [] 
        return lista

    def finalimg(self,host):
        imagen = None
        if '.local' in host:
            ruta = 'http://'
        else:
            ruta = 'https://'

        imgsrc = self.mediapromo_set.filter(tipoimg='imagenfinal').first()
        if imgsrc:
            imagen = '%s%s/%s'%(ruta,host,imgsrc.imagen.name)
        else:
            imagen='null'

        return imagen

    def finalimg_min(self,host):
        imagen = None
        
        imgsrc = self.mediapromo_set.filter(tipoimg='minfinal').first()
        if '.local' in host:
            ruta = 'http://'
        else:
            ruta = 'https://'

        if imgsrc:
            imagen = '%s%s/%s'%(ruta,host,imgsrc.imagen.name)
        else:
            imagen = 'null'
        return imagen


    def galeria(self,host):
        gal = []

        if '.local' in host:
            ruta = 'http://'
        else:
            ruta = 'https://'

        g = self.mediapromo_set.all().exclude(tipoimg__in=['imagenfinal','minfinal','puzzle'])
        for x in g:
            arrg = {'imagen':'%s%s/%s'%(ruta,host,x.imagen.name),'ipk':x.pk}
            gal.append(arrg)
        return gal


    def terminosdeladinamica(self):
        try:
            terminos = Dinamicaterminos.objects.filter(dinamicaslug=self.dinamica).first().terminos

        except:
            terminos = ''

        return terminos


    def descpdeladinamica(self):
        try:
            terminos = Dinamicaterminos.objects.filter(dinamicaslug=self.dinamica).first().descp

        except:
            terminos = ''

        return terminos





class Mediapromo(models.Model):
    promo=models.ForeignKey(Promocion)
    imagen = models.ImageField(upload_to='static/media/promomedia/')
    tipoimg = models.CharField(max_length=100,blank=True,null=True)



class Promocat(models.Model):
    catname = models.CharField(max_length=200,default='categoria')
    catslug = models.CharField(max_length=200,default='categoria')
    parentcat = models.ForeignKey('Promocat',blank=True,null=True)
    orden = models.IntegerField(default=0)

   
class Catpromo(models.Model):
    categoria = models.ForeignKey(Promocat)
    promocion = models.ForeignKey(Promocion)


class Segmento(models.Model):
    segmento = models.CharField(max_length=200,default='amigo')
    slug = models.CharField(max_length=200,default='categoria')
    orden = models.IntegerField(default=0)




# DINAMICAS -----------------------------------------------------------------------------

class Tablerosopa(models.Model):
    promopk = models.ForeignKey(Promocion)
    matrix = models.TextField(blank=True,null=True)
    posiciones = models.TextField(blank=True,null=True)

    def lamatriz(self):
        try:
            if self.matrix:
                matx = self.matrix
            else:
                matx = {}
        except:
            matx = None
        return matx



class Pregunta(models.Model):
    imagen = models.ImageField(upload_to='static/media/promocion/',blank=True,null=True)
    pregunta = models.TextField()
    owners = models.ForeignKey(Promocion)
    orden = models.IntegerField(default=1)


class Dinpalabra(models.Model):
    promopk = models.ForeignKey(Promocion)
    imagen_uno = models.ImageField(upload_to='static/media/imtrivs/',blank=True,null=True)
    imagen_dos = models.ImageField(upload_to='static/media/imtrivs/',blank=True,null=True)
    palabra = models.CharField(max_length=200)
    description = models.TextField(blank=True,null=True)
    tiempo = models.CharField(max_length=200,blank=True,null=True)



class Dinfutbol(models.Model):
    promopk = models.ForeignKey(Promocion)
    imagen_uno = models.ImageField(upload_to='static/media/dinfutbol/',blank=True,null=True)
    imagen_dos = models.ImageField(upload_to='static/media/dinfutbol/',blank=True,null=True)
    marcador_uno = models.CharField(max_length=50,blank=True,null=True)
    marcador_dos = models.CharField(max_length=50,blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    respuesta = models.CharField(max_length=5,blank=True,null=True)
    tiempo = models.CharField(max_length=200,blank=True,null=True)



class Respuesta(models.Model):
    resp = models.CharField(max_length=500)
    cor = models.CharField(max_length=10,blank=True,null=True,default='false')
    pregunta = models.ForeignKey(Pregunta)
    indice = models.CharField(max_length=5,default='A')


class Delikes(models.Model):
    promopk = models.ForeignKey(Promocion)
    userpk = models.ForeignKey(User)
    date_like = models.DateTimeField(auto_now_add=True)

class Participacion(models.Model,TimeMets):
    promopk = models.ForeignKey(Promocion)
    usuario = models.ForeignKey(User)
    tiempo = models.CharField(max_length=100,blank=True,null=True)
    inicio = models.DateTimeField(auto_now_add=True)
    final = models.DateTimeField(blank=True,null=True)
    nivelanswer = models.IntegerField(blank=True,null=True)
    acepta_terminos = models.BooleanField(default=True)
    ganadora = models.BooleanField(default=False)
    fecha_ganador = models.DateTimeField(blank=True,null=True)
    usuario_asigna_ganador = models.IntegerField(blank=True,null=True)


    def dinamicaganadores(self):
        if self.ganadora == True:
            a = 1
        else:
            a = 0
        return a

    def totalpreg(self):
        total = self.resparticipacion_set.all().count()
        return total

    def tiempoJuega(self):
        if self.inicio and self.final:
            tiempojuega = self.final - self.inicio
            
        else:
            tiempojuega = 'no termino'
        return tiempojuega

    def imagenuser(self):
        toimg = self.usuario.profileuser_set.all().first()
        if toimg:
            img = toimg.imagen.name
        else:
            img = None

        return img


    def servicios_usuario(self):
        servicios = self.usuario.profileuser_set.all().first()
        if servicios:
            return servicios.servicios
        else:
            return ''


    def finicio(self):
        try:
            inicial = self.fecha_to_str(self.inicio,formato='%b. %d | %Y | %X')
        except:
            inicial = ''
        return inicial


    def ffinal(self):
        try:
            inicial = self.fecha_to_str(self.final,formato='%b. %d | %Y | %X')
        except:
            inicial = ''
        return inicial




class Partiwin(models.Model):
    partipk = models.ForeignKey(Participacion)
    lugar = models.IntegerField()



class Resparticipacion(models.Model):
    parti = models.ForeignKey(Participacion)
    pregunta = models.IntegerField()
    respuesta = models.IntegerField()
    typo = models.CharField(max_length=50,default='trivia')
    date_add = models.DateTimeField(auto_now_add=True)


class Respondepalabras(models.Model):
    parti = models.ForeignKey(Participacion)
    pregunta = models.IntegerField()
    respuesta = models.CharField(max_length=255,blank=True,null=True)
    date_add = models.DateTimeField(auto_now_add=True)


    def pregunta_txt(self):
        pr =  Pregunta.objects.get(pk=self.pregunta)
        if pr:
            return pr.pregunta
        else:
            return None

    def respuesta_txt(self):
        pr =  Respuesta.objects.get(pk=self.respuesta)
        if pr:
            if pr.cor=='True':
                acerto = 'Correcto'
            else:
                acerto = 'Incorrecto'
            return '%s %s' %(pr.resp,acerto)
        else:
            return None


class Respondefutbol(models.Model):
    dinfut = models.ForeignKey(Dinfutbol)
    marcador_uno = models.CharField(max_length=10)
    marcador_dos = models.CharField(max_length=10)
    respuesta = models.CharField(max_length=5)


# DINAMICAS NUEVAS junio 2018 --------------------------------------------------------

class Swippregunta(models.Model):
    promopk = models.ForeignKey(Promocion)
    pregunta = models.CharField(max_length=200)
    orden = models.IntegerField(default=1)

class Swipimages(models.Model):
    prgeuntapk = models.ForeignKey(Swippregunta)
    imagen = models.ImageField(upload_to='static/statics/swipers')
    sideimg = models.CharField(max_length=10,default='right')
    orden = models.IntegerField(default=1)



class Dinamicaterminos(models.Model):
    dinamicaslug = models.CharField(max_length=100)
    dinamica_name = models.CharField(max_length=200)
    terminos = models.TextField(blank=True,null=True)
    descp = models.TextField(blank=True,null=True)