from django.contrib import admin
from .models import Garment, Outfit, CustomUser

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Garment)
admin.site.register(Outfit)

