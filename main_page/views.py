from django.shortcuts import render
from .models import Materials


def index(request):
    return render(request, 'main_page/index.html')


def materials(request):
    material = Materials.objects.order_by('name')
    return render(request, 'main_page/materials.html', {'title': 'Materials', 'materials': material})


def calculations(request):
    return render(request, 'main_page/calculations.html', {'title': 'Calculations'})


def private_office(request):
    return render(request, 'main_page/private_office.html', {'title': 'Private office'})
