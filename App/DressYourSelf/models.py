from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, max_length=254)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)

    def __str__(self):
        return self.username


# Create your models here.
class Garment(models.Model):
    class Category(models.TextChoices):
        TOP = 'T', _('Top')
        BOTTOM = 'B', _('Bottom')
        DRESS = 'D', _('Dress')
        OUTERWEAR = 'O', _('Outerwear')
        UNDERGARMENTS = 'U', _('Undergarments')
        ACCESSORIES = 'A', _('Accessories')
        FOOTWEAR = 'F', _('Footwear')
        ACTIVEWEAR = 'AW', _('Activewear')
        SWIMWEAR = 'SW', _('Swimwear')
        SLEEPWEAR = 'SL', _('Sleepwear')
        FORMAL_WEAR = 'FW', _('Formal wear')
        INTIMATES = 'I', _('Intimates')
        COSTUME = 'C', _('Costume')
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='garments/')
    description = models.TextField()
    category = models.CharField(max_length=2, choices=Category.choices, default=Category.COSTUME)
    brand = models.CharField(max_length=100, null=True)
    size = models.CharField(max_length=100, null=True)
    color = models.CharField(max_length=100, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        unique_together = ['name', 'user']


class Outfit(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    garments = models.ManyToManyField(Garment)
    image = models.ImageField(upload_to='outfits/')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        unique_together = ['name', 'user']
