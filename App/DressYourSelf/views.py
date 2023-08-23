from django.shortcuts import render
from .models import Garment, Outfit
from django.http import HttpResponse
from django.contrib.auth.models import User

def home(request):
    return HttpResponse('This is the home page!')

# Create your views here.
def add_garment(request):
    if request.method == 'GET':
        categories = Garment.Category.choices
        print(categories)
        return render(request, 'add_garment.html', {
            'categories': categories
        })
    elif request.method == 'POST':
        name = request.POST.get('name')
        image = request.FILES.get('image')
        description = request.POST.get('description')
        category = request.POST.get('category')
        brand = request.POST.get('brand')
        size = request.POST.get('size')
        color = request.POST.get('color')
        user = User.objects.get(username='root')
        try:
            garment = Garment.objects.create(
                name=name,
                image=image,
                description=description,
                category=category,
                brand=brand,
                size=size,
                color=color,
                user=user
            )

            return HttpResponse('Garment added!')
        except Exception as e:
            return HttpResponse('Error adding garment: ' + str(e))
        