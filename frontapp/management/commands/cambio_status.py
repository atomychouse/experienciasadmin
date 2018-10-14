# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
import os
from dinamicasapp.models import *
from PIL import Image
from django.conf import settings
from django.core.files.base import ContentFile


class Command(BaseCommand):
    help = "thumbnail banco Imgs"
    basedir = settings.BASE_DIR


    def handle(self, *args,**options):
        hoy = datetime.datetime.now()
        pr = Promocion.objects.filter(status='proximamente',fecha_publicacion__lte=hoy)
        
        for p in pr:
            p.status='publish'
            p.save()

        return None

