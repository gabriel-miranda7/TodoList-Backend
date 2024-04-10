from django.shortcuts import render
from django.http import HttpResponse


def taskList(req):
    return HttpResponse('To do List')