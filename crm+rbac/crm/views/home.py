from django.shortcuts import render, HttpResponse, redirect, reverse


def index(request):
    return render(request,'index.html')
