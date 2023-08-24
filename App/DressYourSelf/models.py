from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


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
    description = models.TextField(null=True)
    category = models.CharField(max_length=2, choices=Category.choices, default=Category.COSTUME)
    brand = models.CharField(max_length=100, null=True)
    size = models.CharField(max_length=100, null=True)
    color = models.CharField(max_length=100, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Outfit(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    garments = models.ManyToManyField(Garment)
    image = models.ImageField(upload_to='outfits/', null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
