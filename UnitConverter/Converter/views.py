from django.shortcuts import render


# Create your views here.

def converter(request):
    return render(request, template_name="unit_converter.html")
