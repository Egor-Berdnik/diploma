from django.forms import model_to_dict
from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.generics import APIView
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from .models import Materials, Producers, MaterialType
from .forms import WallForm
from .templates import *
from .serializers import MaterialsSerializer, ProducersSerializer, MaterialTypeSerializer


def index(request):
    return render(request, 'main_page/index.html')


class MaterialsAPIView(generics.ListAPIView):
    serializer_class = MaterialsSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'main_page/materials.html'

    def get(self, request):
        m = Materials.objects.all()
        return Response({'posts': MaterialsSerializer(m, many=True).data})

    def post(self, request):
        serializer = MaterialsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'post': serializer.data})

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'error': 'Method PUT not allowed'})

        try:
            instance = Materials.objects.get(pk=pk)
        except:
            return Response({'error': 'Object does not exist'})

        serializer = MaterialsSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'post': serializer.data})

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'error': 'Method DELETE not allowed'})

        try:
            record = Materials.objects.filter(pk=pk)
            record.delete()
        except:
            return Response({'error': "Object does not exist"})

        return Response({'post': 'delete post ' + str(pk)})

    def get_context_data(self, *args, **kwargs):
        context = {
            'materials' : MaterialsSerializer.get_value(self, *args, **kwargs),
        }
        return context


class ProducersAPIList(generics.ListCreateAPIView):
    queryset = Producers.objects.all()
    serializer_class = ProducersSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'main_page/producers.html'

    def get(self, request):
        m = Producers.objects.all()
        return Response({'posts': ProducersSerializer(m, many=True).data})


class ProducersAPIUpdate(generics.UpdateAPIView):
    queryset = Producers.objects.all()
    serializer_class = ProducersSerializer


class ProducersAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Producers.objects.all()
    serializer_class = ProducersSerializer


class MaterialTypeViewSet(viewsets.ModelViewSet):
    queryset = MaterialType.objects.all()
    serializer_class = MaterialTypeSerializer


def calculations(request):
    """
    Функция получает параметры из формы WallForm, затем производится расчет произведения
    параметров width и height. Далее идет условие: если были введены параметры width_of_door
    и height_of_door, считается их произведение и вычитается из рассчитанного выше параметра
    square. Далее задается параметр total_square равный нулю и к нему прибавлются все
    расчитанные значения squar. В результате total_square перемножается на параметр
    cost_of_material, который передается из модели Materials и получается итоговый
    результат result_price.
    В части else передается условие: при окончании сессии вычислений сохраненные результаты
    удаляются для нового рассчета.
    """
    if request.method == "POST":
        width = float(request.POST.get("width"))
        height = float(request.POST.get("height"))
        width_of_door = float(request.POST.get("width_of_door") or 0)
        height_of_door = float(request.POST.get("height_of_door") or 0)
        cost_of_material = float(request.POST.get("cost_of_material"))

        square = width * height
        if width_of_door > 0 and height_of_door > 0:
            square_of_door = width_of_door * height_of_door
            square -= square_of_door

        total_square = request.session.get('total_square', 0)
        total_square += square
        request.session['total_square'] = total_square

        result_price = total_square * cost_of_material
        return render(request, "main_page/calculations.html",
                      {"form": WallForm, 'square': square,
                       'total_square': total_square, 'result_price': result_price})

    else:
        request.session.pop('total_square', None)
        form = WallForm()

    return render(request, "main_page/calculations.html", {"form": form})


def private_office(request):
    return render(request, 'main_page/private_office.html', {'title': 'Private office'})
