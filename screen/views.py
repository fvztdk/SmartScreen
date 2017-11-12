# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from screen import photos_list


def index(request):
    photosList = photos_list.getPhotos()
    context = {
        'photosList': photosList,
    }
    return render(request,'screen/index.html', context )
