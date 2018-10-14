# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User,Group
import simplejson
from django.contrib.sites.models import Site
from django.db.models import Count
import os




class Color(models.Model):
    sitio = models.ForeignKey(Site)
    color = models.CharField(max_length=100,default='')
    rgbcolor = models.CharField(max_length=100,default='')
    tipo = models.CharField(max_length=100,blank=True,null=True)
    orden = models.IntegerField(default=1)

class Combinacion(models.Model):
    sitio = models.ForeignKey(Site)
    fontcolor = models.CharField(max_length=20)
    backcolor = models.CharField(max_length=20)
    visible = models.BooleanField(default=True)


class Tipografia(models.Model):
    sitio = models.ForeignKey(Site)
    tipofile = models.FileField(upload_to='static/media/cfg_files')
    uso = models.CharField(max_length=50)
    puntaje = models.CharField(max_length=10)

    def namefont(self):
        filename = self.tipofile.name.split('/')[-1]
        name = filename.split('.')[0]

        return name



class Sitesetting(models.Model):
    sitio = models.ForeignKey(Site)
    tiposet = models.CharField(max_length=100,default='')
    valueset = models.CharField(max_length=200,default='')

    def colorsets(self):
        color = simplejson.loads(self.valueset)

        return color