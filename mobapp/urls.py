# -*- coding: utf-8 -*-

from django.conf.urls import url,patterns
from . import views as MViews 
from django.contrib.auth.decorators import login_required, permission_required


urlpatterns = [
   
   url(r'^categorias/$',(MViews.Cats), name='categorias'),
   url(r'^promos/$',(MViews.promoList), name='promos'),
   url(r'^addlikes/$',(MViews.addLike), name='addlikes'),
   url(r'^finalizados/$',(MViews.promoEnd), name='finalizados'),
   url(r'^promosby/$',(MViews.promoSear), name='promosby'),
   url(r'^reguser/$',(MViews.rergUser), name='reguser'),
   url(r'^reg_tel_user/$',(MViews.regTelUser), name='reg_tel_user'),
   url(r'^getuser/$',(MViews.getUser), name='getuser'),
   url(r'^getprofileuser/$',(MViews.getProfileUser), name='getprofileuser'),
   url(r'^fotoperfil/$',(MViews.fotoPerfil), name='fotoperfil'),
   url(r'^settuser/$',(MViews.settUser), name='settuser'),   
   url(r'^rmserviceuser/$',(MViews.removeServiceUser), name='rmserviceuser'),   
   url(r'^promocion/(?P<pks>[\w-]+)/$',(MViews.promoDetail), name='promocion'),     
   url(r'^participando/(?P<uspk>[\w-]+)/(?P<promopk>[\w-]+)/$',(MViews.Participandome), name='participando'),   
   url(r'^finaltrivia/$',(MViews.FinalTrivia), name='finaltrivia'),   
   url(r'^finalpalabras/$',(MViews.FinalPalabras), name='finalpalabras'),
   url(r'^finalfutbol/$',(MViews.FinalFutbol), name='finalfutbol'),   
   url(r'^finalpanorama/(?P<uspk>[\w-]+)/(?P<promopk>[\w-]+)/$',(MViews.Finalpanorama), name='finalpanorama'),
   url(r'^finalsopa/(?P<uspk>[\w-]+)/(?P<promopk>[\w-]+)/$',(MViews.FinalSopa), name='finalsopa'),
   url(r'^finalpuzz/(?P<uspk>[\w-]+)/(?P<promopk>[\w-]+)/$',(MViews.FinalPuzz), name='finalpuzz'),
   url(r'^finalswiper/(?P<uspk>[\w-]+)/(?P<promopk>[\w-]+)/$',(MViews.FinalSwip), name='finalswiper'),






]

