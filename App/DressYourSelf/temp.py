from django.core.files.storage import default_storage
import os
from django.conf import settings


def delete_temporary_image(temporary_image_path):
    if default_storage.exists(temporary_image_path):
        default_storage.delete(temporary_image_path)
        print("Deleted temporary image: ", temporary_image_path)


def upload_image(name, contentFile):
    filename = default_storage.save(os.path.join("uploaded_images", name), contentFile)
    return default_storage.url(filename), os.path.join("uploaded_images", name)

