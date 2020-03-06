from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'core/index.html')

def shop(request):
    return render(request, 'core/shop.html')