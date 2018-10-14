# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
import os
from dinamicasapp.models import *
from PIL import Image
from django.conf import settings
from django.core.files.base import ContentFile
import xlsxwriter


class Command(BaseCommand):
    help = "thumbnail banco Imgs"
    basedir = settings.BASE_DIR


    def handle(self, *args,**options):

        pr = Promocion.objects.all()
        
        for p in pr:
            print p
            		

        return None

