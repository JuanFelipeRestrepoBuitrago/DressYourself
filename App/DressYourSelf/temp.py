from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os


def delete_temporary_image(temporary_image_path):
    os.remove(temporary_image_path)


def upload_image(image):
    filename = default_storage.save('uploaded_images/' + image.name, ContentFile(image.read()))
    return default_storage.url(filename)

