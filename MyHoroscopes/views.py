from django.http import HttpResponse
from django.shortcuts import render, redirect

def RajHoroscopicSignDetailView(request):
    return redirect('/RajAstrologySigns/')