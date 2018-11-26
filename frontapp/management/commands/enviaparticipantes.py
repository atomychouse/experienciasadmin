# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
import os
from dinamicasapp.models import *
from PIL import Image
from django.conf import settings
from django.core.files.base import ContentFile
import xlsxwriter
import pytz
from django.contrib.auth.models import User,Group
from django.core.mail import send_mail, EmailMessage
from mobapp.views import TimeMets
from django.db.models import Q

class Command(BaseCommand,TimeMets):
    help = "thumbnail banco Imgs"
    basedir = settings.BASE_DIR


    def add_arguments(self, parser):
        parser.add_argument('pid', nargs='+', type=int, help='PROMO ID')

    def handle(self, *args,**options):
        ppk = options['pid']

        mxtz = pytz.timezone('America/Mexico_City')
        hoy = datetime.datetime.now(mxtz) + datetime.timedelta(days=1)

        if ppk[0]==0:
            pr = Promocion.objects.filter(vigencia=hoy,reporte_enviado__isnull=True)
            print 'todas'
        else:
            pr = Promocion.objects.filter(pk=ppk[0])
            print 'especifico'



        assert False,hoy


        for promo in pr:
            
            parti = promo.participacion_set.all().order_by('-nivelanswer')
            parti = Participacion.objects.filter(promopk=promo,final__isnull=False).order_by('-nivelanswer','tiempo')
            promo.reporte_enviado=1
            promo.save()

            filepad = '%s/frontapp/envios/promo_%s.xlsx' %(settings.BASE_DIR,promo.pk)
            f= open(filepad,"w+")
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
            f.close()

            mail = EmailMessage(u'%s %s'%(promo.linea_uno,promo.linea_dos), u'Resultados de la promo: Hola, Te hago llegar los resultados de la promoción, %s %s'%(promo.linea_uno,promo.linea_dos), 'admin@experienciastelcel.com',['albertorios.py@gmail.com','diego.navarro@santamarca.com.mx','mariela.ramirez@santamarca.com.mx','carlos.godoy@santamarca.com.mx','ernesto.romero@santamarca.com.mx'],)
            mail.attach_file('%s/frontapp/envios/promo_%s.xlsx' %(settings.BASE_DIR,promo.pk))
            mail.send()


        promociones = Promocion.objects.filter((Q(status='publish') & Q(vigencia__gte=hoy) ) | Q(status='proximamente') )
        print len(promociones)


        return None

