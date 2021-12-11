from django.core.files import storage
from django.db import models
from django.conf import settings
from djongo import models
from djongo.storage import GridFSStorage


BASE_URL = 'http://127.0.0.1:8000/'

class register(models.Model):
    emp_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    grid_fs_storage = GridFSStorage(collection='images_Data', base_url=''.join([BASE_URL, 'images_Data/']))
    image = models.ImageField( storage=grid_fs_storage )
  
    def __str__(self):
        return self.name
    