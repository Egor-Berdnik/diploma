from django.shortcuts import render
from .models import Materials, Producers
from .forms import WallForm


def calculations(request):
    if request.method == "POST":
        width = int(request.POST.get("width"))
        height = int(request.POST.get("height"))
        cost_of_material = int(request.POST.get("cost_of_material"))
        square = width * height
        result_price = square * cost_of_material
        return render(request, "main_page/calculations.html", {"form": WallForm, 'square': square,
                                                               'result_price': result_price})
    else:
        return render(request, "main_page/calculations.html", {"form": WallForm})


def index(request):
    return render(request, 'main_page/index.html')


def materials(request):
    material = Materials.objects.order_by('name')
    return render(request, 'main_page/materials.html', {'title': 'Materials', 'materials': material})


# def calculations(request):
#     return render(request, 'main_page/calculations.html', {'title': 'Calculations'})


def private_office(request):
    return render(request, 'main_page/private_office.html', {'title': 'Private office'})


def producers(request):
    producer = Producers.objects.order_by('name')
    return render(request, 'main_page/producers.html', {'title': 'Producers', 'producers': producer})
