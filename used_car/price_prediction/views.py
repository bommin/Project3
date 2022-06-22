from django.shortcuts import render
from .connectDB import *
# Create your views here.
from .get_graph import *


def index(request):
    if request.method == 'GET':
        return render(request, 'index.html')
    if request.method == 'POST':
        manufacturer = request.POST['manufacturer']
        fuel = request.POST['fuel']
        simple = request.POST['simple']
        year = request.POST['year']
        cc = request.POST['cc']
        km = request.POST['km']
        og = request.POST['og']
        deep = deeplearning_response(
            manufacturer, fuel, simple, year, cc, km, og)
        predict = predict_response(
            manufacturer, fuel, simple, year, cc, km, og)
        var_graph = get_graph(simple, fuel, year)
        context = {'predict_price': predict,
                   'deep': deep, 'var_graph': var_graph}
        return render(request, 'index.html', context=context)


def graph(request):
    if request.method == 'GET':
        return render(request, 'graph.html')
    if request.method == 'POST':
        fuel = request.POST['fuel']
        simple = request.POST['simple']
        year = request.POST['year']
        var_graph = get_graph(simple, fuel, year)
        context = {'var_graph': var_graph}
        return render(request, 'graph.html', context=context)


def home(request):

    return render(request, 'home.html')
