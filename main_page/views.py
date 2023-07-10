from django.http import QueryDict
from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.generics import APIView
from rest_framework import generics, viewsets, status
from rest_framework.renderers import TemplateHTMLRenderer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .models import Materials, Producers, MaterialType
from .forms import WallForm
from .serializers import MaterialsSerializer, ProducersSerializer, MaterialTypeSerializer
from.tasks import *
from .serializers import MaterialsSerializer, ProducersSerializer, MaterialTypeSerializer, PutSerializer, WallSerializer


def index(request):
    return render(request, 'main_page/index.html')


class MaterialsAPIView(generics.ListAPIView):
    serializer_class = MaterialsSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'main_page/materials.html'

    def get(self, request):
        materials = Materials.objects.all()
        serializer = MaterialsSerializer(materials, many=True)
        return Response({'posts': serializer.data})

    def post(self, request):
        serializer = MaterialsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'post': serializer.data})

    def put(self, request, *args, **kwargs):
        pk = self.get_validated_pk(kwargs)
        material = self.get_material(pk)

        serializer = self.get_material_serializer(request.data, material)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'post': serializer.data})

    def delete(self, request, *args, **kwargs):
        pk = self.get_validated_pk(kwargs)
        material = self.get_material(pk)
        material.delete()
        return Response({'post': f'delete post {pk}'}, status=status.HTTP_204_NO_CONTENT)

    def get_context_data(self, *args, **kwargs):
        context = {
            'materials': self.serializer_class.get_value(self, *args, **kwargs),
        }
        return context

    def get_validated_pk(self, kwargs):
        serializer = PutSerializer(data=kwargs)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data['pk']

    def get_material(self, pk):
        return get_object_or_404(Materials, pk=pk)

    def get_material_serializer(self, data, instance=None):
        return MaterialsSerializer(data=data, instance=instance)


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

    def producers_list(request):
        producer = Producers.objects.all()
        return render(request, 'producer_detailed.html', {'producer': producer})


class MaterialTypeViewSet(viewsets.ModelViewSet):
    queryset = MaterialType.objects.all()
    serializer_class = MaterialTypeSerializer


def calculations(request):
    """
        The function receives parameters from the WallForm form and then calculates the product
    of the width and height parameters. It then checks if the width_of_door and height_of_door
    parameters were entered, calculates their product, and subtracts it from the previously
    calculated square. Next, a total_square parameter is set to zero and all calculated
    square values are added to it. The total_square is then multiplied by the cost_of_material
    parameter, which is passed from the Materials model, resulting in the final result_price.
        In the else part, there is a condition to remove the saved calculation results when
    the calculation session is finished, in order to start fresh for a new calculation.
    """
    form = WallForm()
    total_square = request.session.get('total_square', 0)
    result_price = request.session.get('result_price', 0)

    if request.method == "POST":
        data = QueryDict(request.body)
        serializer = WallSerializer(data=data)

        if serializer.is_valid():
            width = serializer.validated_data.get("width")
            height = serializer.validated_data.get("height")
            width_of_door = serializer.validated_data.get("width_of_door") or 0
            height_of_door = serializer.validated_data.get("height_of_door") or 0
            cost_of_material = serializer.validated_data.get("cost_of_material")

            square = width * height
            if width_of_door > 0 and height_of_door > 0:
                square_of_door = width_of_door * height_of_door
                square -= square_of_door

            total_square += square
            request.session['total_square'] = total_square

            price = square * cost_of_material

            result_price += price
            request.session['result_price'] = result_price

            return render(request, "main_page/calculations.html",
                          {"form": WallForm(), 'square': square,
                           'total_square': total_square, 'result_price': result_price})

    else:
        request.session.pop('total_square', None)
        request.session.pop('result_price', None)

    return render(request, "main_page/calculations.html", {"form": form})


def private_office(request):
    return render(request, 'main_page/private_office.html', {'title': 'Private office'})


def your_view(request):
    some_task.apply_async()


class RunTaskView(APIView):
    def post(self, request):
        some_task.delay()
        test_scheduled_task.delay('Some parameter')
        return Response({'status': 'success'})