from django.db import transaction, IntegrityError
from django.db.models import Q
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Outfit, Garment, CustomUser
from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from .forms import CustomUserChangeForm, CustomPasswordChangeForm
from .generation import APIs, get_outfit_caption, get_outfit
from .temp import *
from django.core.files.base import ContentFile
import openai
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt



apis = APIs()


def get_garments_by_category(method):
    if method.get('tops') == '' or method.get('tops') is None or method.get('tops') == ' ':
        tops = None
    else:
        tops = method.get('tops')
        if tops[-1] == ',' or tops[-1] == ', ' or tops[-1] == ' ':
            tops = tops[:-1]
        tops = tops.split(',')
        tops = Garment.objects.filter(id__in=tops)

    if method.get('bottoms') == '' or method.get('bottoms') is None or method.get(
            'bottoms') == ' ':
        bottoms = None
    else:
        bottoms = method.get('bottoms')
        if bottoms[-1] == ',' or bottoms[-1] == ', ' or bottoms[-1] == ' ':
            bottoms = bottoms[:-1]
        bottoms = bottoms.split(',')
        bottoms = Garment.objects.filter(id__in=bottoms)

    if method.get('footwears') == '' or method.get('footwears') is None or method.get(
            'footwears') == ' ':
        footwears = None
    else:
        footwears = method.get('footwears')
        if footwears[-1] == ',' or footwears[-1] == ', ' or footwears[-1] == ' ':
            footwears = footwears[:-1]
        footwears = footwears.split(',')
        footwears = Garment.objects.filter(id__in=footwears)

    if method.get('others') == '' or method.get('others') is None or method.get(
            'others') == ' ':
        others = None
    else:
        others = method.get('others')
        if others[-1] == ',' or others[-1] == ', ' or others[-1] == ' ':
            others = others[:-1]
        others = others.split(',')
        others = Garment.objects.filter(id__in=others)

    return tops, bottoms, footwears, others


# Create your views here.
@login_required
def add_garment(request):
    if request.method == 'GET':
        categories = Garment.Category.choices
        return render(request, 'add_garment.html', {
            'categories': categories,
            'cssBootstrap': False,
            'jsBootstrap': True,
            'cssName': '/css/add_garment.css',
            'jsName': '/js/add_garment.js'
        })
    elif request.method == 'POST':
        try:
            if request.POST.get('name') == '' or request.POST.get('name') is None or request.POST.get('name') == ' ':
                raise IntegrityError('Name is required')
            else:
                name = request.POST.get('name')
            if request.POST.get('category') == '' or request.POST.get('category') is None or request.POST.get(
                    'category') == ' ':
                raise IntegrityError('Category is required')
            else:
                category = request.POST.get('category')
            image = request.FILES.get('image')
            if request.POST.get('description') == '' or request.POST.get('description') is None or request.POST.get(
                    'description') == ' ':
                description = apis.get_caption(image)
            else:
                description = request.POST.get('description')
                if len(description) < 15:
                    raise IntegrityError('Description must be at least 15 characters long')
            if request.POST.get('brand') == '' or request.POST.get('brand') is None or request.POST.get('brand') == ' ':
                brand = None
            else:
                brand = request.POST.get('brand')
            if request.POST.get('size') == '' or request.POST.get('size') is None or request.POST.get('size') == ' ':
                size = None
            else:
                size = request.POST.get('size')
            if request.POST.get('color') == '' or request.POST.get('color') is None or request.POST.get('color') == ' ':
                color = None
            else:
                color = request.POST.get('color')
            user = request.user

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

            garment.save()

            return redirect('garments')
        except IntegrityError as e:
            if e.args[0] == 'UNIQUE constraint failed: DressYourSelf_garment.name, DressYourSelf_garment.user_id':
                messages.error(request, "The name of the garment is already taken")
            else:
                messages.error(request, e)
            return redirect('add_garment')


@login_required
@transaction.atomic
def garments(request):
    garments_clothes = Garment.objects.filter(user=request.user)
    if request.method == 'GET':
        return render(request, 'garments.html', {
            'cssBootstrap': False,
            'jsBootstrap': False,
            'garments': garments_clothes,
            'cssName': '/css/garments.css',
            'jsName': '/js/garments.js'
        })
    elif request.method == 'POST':
        try:
            identification = request.POST.get('id')
            garment = Garment.objects.get(id=identification)
            garment.delete()
            return redirect('garments')
        except IntegrityError as e:
            messages.error(request, e)
            return redirect('garments')


@login_required
@transaction.atomic
def edit_garment(request, identification):
    garment = Garment.objects.get(id=identification)
    if request.method == 'GET':
        categories = Garment.Category.choices
        return render(request, 'edit_garment.html', {
            'categories': categories,
            'cssBootstrap': False,
            'jsBootstrap': True,
            'garment': garment,
            'cssName': '/css/add_garment.css',
            'jsName': '/js/add_garment.js'
        })
    elif request.method == 'POST':
        try:
            if request.POST.get('name') == '' or request.POST.get('name') is None or request.POST.get('name') == ' ':
                raise IntegrityError('Name is required')
            else:
                name = request.POST.get('name')
            if request.POST.get('category') == '' or request.POST.get('category') is None or request.POST.get(
                    'category') == ' ':
                raise IntegrityError('Category is required')
            else:
                category = request.POST.get('category')
            if request.FILES.get('image') is None:
                image = garment.image
            else:
                image = request.FILES.get('image')
            if request.POST.get('description') == '' or request.POST.get('description') is None or request.POST.get(
                    'description') == ' ':
                description = apis.get_caption(image)
            else:
                description = request.POST.get('description')
                if len(description) < 15:
                    raise IntegrityError('Description must be at least 15 characters long')
            if request.POST.get('brand') == '' or request.POST.get('brand') is None or request.POST.get('brand') == ' ':
                brand = None
            else:
                brand = request.POST.get('brand')
            if request.POST.get('size') == '' or request.POST.get('size') is None or request.POST.get('size') == ' ':
                size = None
            else:
                size = request.POST.get('size')
            if request.POST.get('color') == '' or request.POST.get('color') is None or request.POST.get('color') == ' ':
                color = None
            else:
                color = request.POST.get('color')
            user = request.user

            garment.name = name
            garment.image = image
            garment.description = description
            garment.category = category
            garment.brand = brand
            garment.size = size
            garment.color = color
            garment.user = user

            garment.save()

            return redirect('garments')
        except IntegrityError as e:
            if e.args[0] == 'UNIQUE constraint failed: DressYourSelf_garment.name, DressYourSelf_garment.user_id':
                messages.error(request, "The name of the garment is already taken")
            else:
                messages.error(request, e)
            return redirect('edit_garment')


@login_required
# Create your views here.
def add_outfit(request):
    tops = Garment.objects.filter(user=request.user, category="Top")
    bottoms = Garment.objects.filter(user=request.user, category="Bottom")
    footwears = Garment.objects.filter(user=request.user, category="Footwear")
    others = Garment.objects.filter(user=request.user).exclude(category="Top").exclude(category="Bottom").exclude(
        category="Footwear")
    if request.method == 'GET':
        return render(request, 'add_outfit.html', {
            'cssBootstrap': False,
            'jsBootstrap': True,
            'cssName': '/css/add_outfit.css',
            'jsName': '/js/add_outfit.js',
            'tops': tops,
            'bottoms': bottoms,
            'footwears': footwears,
            'others': others
        })
    elif request.method == 'POST':
        try:
            if request.POST.get('name') == '' or request.POST.get('name') is None or request.POST.get('name') == ' ':
                raise IntegrityError('Name is required')
            else:
                name = request.POST.get('name')

            if request.FILES.get('outfitImage') is None or request.FILES.get('outfitImage') == '' or request.FILES.get('outfitImage') == ' ':
                raise FileNotFoundError('Image is required')
            else:
                image = request.FILES.get('outfitImage')

            if request.POST.get('description') == '' or request.POST.get('description') is None or request.POST.get(
                    'description') == ' ':
                description = None
            else:
                description = request.POST.get('description')

            tops, bottoms, footwears, others = get_garments_by_category(request.POST)

            user = request.user
            outfit = Outfit.objects.create(
                name=name,
                image=image,
                description=description,
                user=user
            )

            if tops is not None:
                outfit.garments.add(*tops)
            if bottoms is not None:
                outfit.garments.add(*bottoms)
            if footwears is not None:
                outfit.garments.add(*footwears)
            if others is not None:
                outfit.garments.add(*others)

            outfit.save()

            return redirect('closet_outfits')
        except IntegrityError:
            messages.error(request, "The name of the outfit is already taken")
            return redirect('add_outfit')
        except FileNotFoundError:
            messages.error(request, "An image is required")
            return redirect('add_outfit')


@login_required
# Create your views here.
def add_outfit_generated(request):
    tops = Garment.objects.filter(user=request.user, category="Top")
    bottoms = Garment.objects.filter(user=request.user, category="Bottom")
    footwears = Garment.objects.filter(user=request.user, category="Footwear")
    others = Garment.objects.filter(user=request.user).exclude(category="Top").exclude(category="Bottom").exclude(
        category="Footwear")
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            description = request.POST.get('description')
            if description is None or description == '' or description == ' ':
                description = None

            if request.FILES.get('outfitImage') is None or request.FILES.get('outfitImage') == '' or request.FILES.get(
                    'outfitImage') == ' ':
                raise FileNotFoundError('Image is required')
            else:
                image = request.FILES.get('outfitImage')
                temp_image_path = upload_image(image.name, ContentFile(image.read()))
            if request.FILES.get('maskImage') is None or request.FILES.get('maskImage') == '' or request.FILES.get(
                    'maskImage') == ' ':
                raise FileNotFoundError('Mask is required')
            else:
                mask = request.FILES.get('maskImage')
                temp_mask_path = upload_image(mask.name, ContentFile(mask.read()))

            selected_tops, selected_bottoms, selected_footwears, selected_others = get_garments_by_category(request.POST)
            captions = get_outfit_caption(selected_tops, selected_bottoms, selected_footwears, selected_others)

            temp_outfit_image = get_outfit(captions, temp_image_path[1], temp_mask_path[1])

            delete_temporary_image(temp_image_path[1])
            return render(request, 'add_outfit.html', {
                'cssBootstrap': False,
                'jsBootstrap': True,
                'cssName': '/css/add_outfit.css',
                'jsName': '/js/add_outfit.js',
                'tops': tops,
                'bottoms': bottoms,
                'footwears': footwears,
                'others': others,
                'name': name,
                'mask': temp_mask_path,
                'image': temp_outfit_image,
                'description': description,
                'selected_tops': selected_tops,
                'selected_bottoms': selected_bottoms,
                'selected_footwears': selected_footwears,
                'selected_others': selected_others
            })
        except FileNotFoundError as e:
            messages.error(request, e)
            return redirect('add_outfit')


@login_required
def save_outfit_generated(request):
    if request.method == "POST":
        try:
            mask = request.POST.get('mask')
            delete_temporary_image(mask)

            if request.POST.get('name') == '' or request.POST.get('name') is None or request.POST.get('name') == ' ':
                raise IntegrityError('Name is required')
            else:
                name = request.POST.get('name')

            image_temp = request.POST.get('image')
            image = default_storage.open(image_temp, "rb").read()

            if request.POST.get('description') == '' or request.POST.get('description') is None or request.POST.get(
                    'description') == ' ':
                description = None
            else:
                description = request.POST.get('description')

            tops, bottoms, footwears, others = get_garments_by_category(request.POST)

            user = request.user
            outfit = Outfit.objects.create(
                name=name,
                description=description,
                user=user
            )
            outfit.image.save("generated_image.png", ContentFile(image))
            delete_temporary_image(image_temp)

            if tops is not None:
                outfit.garments.add(*tops)
            if bottoms is not None:
                outfit.garments.add(*bottoms)
            if footwears is not None:
                outfit.garments.add(*footwears)
            if others is not None:
                outfit.garments.add(*others)

            outfit.save()

            return redirect('closet_outfits')
        except IntegrityError:
            messages.error(request, "The name of the outfit is already taken")
            return redirect('add_outfit')


def generate_random_outfit(request):
    
    if request.method == 'POST':
        
        # Recupera los datos del formulario enviado
        name = request.POST.get('name')
        description = request.POST.get('description')
        image = request.FILES.get('outfitImage')
        tops = request.POST.getlist('tops')  # En tu formulario, esto debe ser un conjunto de checkbox
        bottoms = request.POST.getlist('bottoms')  # En tu formulario, esto debe ser un conjunto de checkbox
        footwears = request.POST.getlist('footwears')  # En tu formulario, esto debe ser un conjunto de checkbox
        others = request.POST.getlist('others')  # En tu formulario, esto debe ser un conjunto de checkbox

        # Crea una instancia de Outfit y guárdala en la base de datos
        outfit = Outfit(name=name, description=description, image=image, user=request.user)
        outfit.save()
        
        

        # Añade los componentes del atuendo al atuendo
        if tops:
            outfit.garments.add(*Garment.objects.filter(id__in=tops))
        if bottoms:
            outfit.garments.add(*Garment.objects.filter(id__in=bottoms))
        if footwears:
            outfit.garments.add(*Garment.objects.filter(id__in=footwears))
        if others:
            outfit.garments.add(*Garment.objects.filter(id__in=others))
            
        
        return redirect('closet_outfits')

    else:
        # Lógica para generar un atuendo aleatorio
        top = Garment.objects.filter(category="Top").order_by('?').first()
        bottom = Garment.objects.filter(category="Bottom").order_by('?').first()
        footwear = Garment.objects.filter(category="Footwear").order_by('?').first()
        other = Garment.objects.exclude(category__in=["Top", "Bottom", "Footwear"]).order_by('?').first()
        
        return render(request, 'random_outfits.html', {
            'top': top,
            'bottom': bottom,
            'footwear': footwear,
            'other': other,
        })


# transaction.atomic() is used to rollback the database if an error occurs
@transaction.atomic
def signin(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'GET':
        return render(request, 'signin.html')
    elif request.method == 'POST':
        try:
            username = CustomUser.objects.all().get(
                Q(username=request.POST.get('username')) | Q(email=request.POST.get('username'))).username
            user = CustomUser.objects.all().get(username=username, password=request.POST.get('password'))

            if user is None:
                messages.error(request, 'Invalid username or password')
                return redirect('signin')
            else:
                login(request, user)
                return redirect('home')
        except CustomUser.DoesNotExist:
            messages.error(request, 'User does not exist')
            return redirect('authentication')
    else:
        return 404


@transaction.atomic
def authentication(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'GET':
        return render(request, 'signup.html')
    elif request.method == 'POST':
        if request.POST['password'] == request.POST['password']:
            try:
                # Creates a new user object
                user = CustomUser.objects.create(username=request.POST['username'], password=request.POST['password'],
                                                 email=request.POST['email'], first_name=request.POST['name'],
                                                 last_name=request.POST['lastname'])
                # Saves the user object
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                messages.info(request, 'Username already taken or email already registered')
                return redirect('authentication')
        else:
            messages.error(request, 'Passwords must match')
            return redirect('authentication')


def home(request):
    if request.user.is_authenticated:
        return render(request, 'new-home.html')
    return render(request, 'home.html')


def signout(request):
    logout(request)
    return redirect('home')


def closet_outfits(request):
    # Obtener el parámetro de búsqueda desde la URL
    search_query = request.GET.get('search')

    # Recuperar todos los outfits del usuario actual
    outfits = Outfit.objects.filter(user=request.user)

    if search_query:
        # Si se proporciona un parámetro de búsqueda, filtrar los outfits por nombre
        outfits = outfits.filter(name__icontains=search_query)

    if request.method == 'POST':
        # Si se envía una solicitud POST, significa que se solicitó eliminar un outfit
        outfit_id = request.POST.get('outfit_id')
        outfit_to_delete = Outfit.objects.get(id=outfit_id)
        outfit_to_delete.delete()
        return redirect('closet_outfits')

    return render(request, 'closet_outfits.html', {'outfits': outfits, 'search_query': search_query})


# vista de profile
@login_required
def edit_user(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Tu perfil ha sido actualizado con éxito.')
            return redirect('home')  # Cambia 'home' a la URL de la página de inicio de tu aplicación
    else:
        form = CustomUserChangeForm(instance=request.user)

    return render(request, 'edit_user.html', {'form': form})


def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request,
                                     user)  # Actualiza la sesión del usuario para evitar que se cierre la sesión
            messages.success(request, 'Tu contraseña ha sido actualizada con éxito.')
            return redirect('home')  # Cambia 'home' a la URL de la página de inicio de tu aplicación
    else:
        form = CustomPasswordChangeForm(request.user)

    return render(request, 'change_password.html', {'form': form})


"""
def edit_user(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(instance=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            # Actualizar la sesión del usuario en caso de que cambie la contraseña
            update_session_auth_hash(request, user)
            messages.success(request, 'Tu perfil ha sido actualizado con éxito.')
            return redirect('home')  # Cambia 'profile' a la URL de la página de perfil del usuario
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'edit_user.html', {'form': form})


def edit_user(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(instance=request.user, data=request.POST)
        password_change_form = PasswordChangeForm(user=request.user, data=request.POST)
        
        if form.is_valid() and password_change_form.is_valid():
            user = form.save()
            password_change_form.save()

            update_session_auth_hash(request, user)

            messages.success(request, 'Tu perfil ha sido actualizado con éxito y tu contraseña ha sido cambiada si proporcionaste una nueva contraseña.')
            return redirect('home')  # Redirigir a la página de inicio
    else:
        form = CustomUserChangeForm(instance=request.user)
        password_change_form = PasswordChangeForm(user=request.user)

    return render(request, 'edit_user.html', {'form': form, 'password_change_form': password_change_form})


def edit_user(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(instance=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            # Actualizar la sesión del usuario en caso de que cambie la contraseña
            update_session_auth_hash(request, user)
            messages.success(request, 'Tu perfil ha sido actualizado con éxito.')
            return redirect('home')  # Cambia 'profile' a la URL de la página de perfil del usuario
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'edit_user.html', {'form': form})
"""
#chatbot

openai.api_key = 'su respectiva api key'


def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,  # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]


def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,  # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]


def collect_messages(prompt, context):
    context.append({'role': 'user', 'content': f"{prompt}"})
    response = get_completion_from_messages(context)
    context.append({'role': 'assistant', 'content': f"{response}"})
    return response


def chat(request):
    context = [{'role': 'system', 'content': """
    You are the virtual assistant of DreesYourSelf, your job is to resolve doubts for clients and be short with the messages/
    DressYourSelf is a platform that simulates a virtual closet and allows its clients to organize their clothes in a virtual environment.
    First you greet the user and offer to answer their questions/
    The operation of the application is as follows, this can help the user tu know how to use the platform/
    In the Add Garments button you can enter the desired garments by uploading images/
    In Garments section it will allow you to see what clothes you have uploaded to the platform and search por specific ones/
    The button Closet will allow you to see your created outfits and will have a search bar/
    Add outfit will be the way to assemble his clothes of the garments you had uppload, match them, see how he looks on himself and generate random outfits/
    In addition to this it has the basic functions of editing profile and forgot password/


    """}]


    return render(request, 'chat.html',)


def get_bot_response(request):
    user_input = request.GET.get('user_input', '')
    context = [{'role': 'system', 'content': """
    You are the virtual assistant of DreesYourSelf, your job is to resolve doubts for clients and be short with the messages/
    DressYourSelf is a platform that simulates a virtual closet and allows its clients to organize their clothes in a virtual environment.
    First you greet the user and offer to answer their questions/
    The operation of the application is as follows, this can help the user tu know how to use the platform/
    In the Add Garments button you can enter the desired garments by uploading images/
    In Garments section it will allow you to see what clothes you have uploaded to the platform and search por specific ones/
    The button Closet will allow you to see your created outfits and will have a search bar/
    Add outfit will be the way to assemble his clothes of the garments you had uppload, match them, see how he looks on himself and generate random outfits/
    In addition to this it has the basic functions of editing profile and forgot password/
    """}]
    response_data = {'assistant_response': collect_messages(user_input, context)}
    return JsonResponse(response_data)