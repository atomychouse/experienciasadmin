# -*- coding: utf-8 -*-

from django.conf.urls import url,patterns
from . import views as MViews 
from django.contrib.auth.decorators import login_required, permission_required


urlpatterns = [
   url(r'^imagen/$',(MViews.ImagenP), name='imagen'),
   url(r'^addmodulo/$',(MViews.addModulo), name='addmodulo'),   
   url(r'^addcategoria/$',(MViews.addCategoria), name='addcategoria'),
   url(r'^additm/$',(MViews.addItm), name='additm'),
   url(r'^savemycats/$',(MViews.saveMyCats), name='savemycats'),
   url(r'^rmitm/$',(MViews.rmItm), name='rmitm'),
   url(r'^rmmod/$',(MViews.rmModulo), name='rmmod'),
   url(r'^rmcat/$',(MViews.rmCat), name='rmcat'),
   url(r'^addfile/$',(MViews.addFile), name='addfile'),
   url(r'^rmfile/$',(MViews.rmFile), name='rmfile'),
   url(r'^savecfg/$',(MViews.saveCfg), name='savecfg'),
   url(r'^savecolumna/$',(MViews.saveColumna), name='savecolumna'),
   #url(r'^savesubpage/$',(MViews.saveSubpage), name='savesubpage'),
   url(r'^savepage/$',(MViews.savePage), name='savepage'),
   url(r'^rmpage/$',(MViews.rmPage), name='rmpage'),
   url(r'^rmcol/$',(MViews.rmColumn), name='rmcol'),
   url(r'^dropimage/$',(MViews.dropImage), name='dropimage'),
   url(r'^dropimagelg/$',(MViews.dropImagelg), name='dropimagelg'),   
   url(r'^addparam/$',(MViews.addParam), name='addparam'),
   url(r'^rmparam/$',(MViews.rmParam), name='rmparam'),
   url(r'^upparam/$',(MViews.upParam), name='upparam'),
   url(r'^addcolor/$',(MViews.addColor), name='addcolor'),
   url(r'^reorder/$',(MViews.Reorder), name='reorder'),
   url(r'^addimagefinal/$',(MViews.AddImage), name='addimagefinal'),
   url(r'^addimagegaleria/$',(MViews.AddImageG), name='addimagegaleria'),
   url(r'^rmgaleria/$',(MViews.rmGaleria), name='rmgaleria'),



   #url(r'^rmcatalogo/$',(MViews.rmCatalogo), name='rmcatalogo'),

]

