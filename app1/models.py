from django.core.files import storage
from django.db import models
from django.conf import settings
from djongo import models
from djongo.models.fields import ArrayField
from djongo.storage import GridFSStorage
from django.apps import apps
import face_recognition
import pymongo
import pickle5 as pickle
import pybase64 as base64

BASE_URL = 'http://127.0.0.1:8000/'


def get_points():
    Task = apps.get_model(app_label='app1', model_name='register')
    return 1234

class register(models.Model):
    emp_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    grid_fs_storage = GridFSStorage(collection='images_Data', base_url=''.join([BASE_URL, 'images_Data/']))
    image = models.ImageField( storage=grid_fs_storage )
    
    def enc_func(self,img):
        known_image = face_recognition.load_image_file(img)
        biden_encoding = face_recognition.face_encodings(known_image)[0]
        return pickle.dumps( biden_encoding )


    def save(self, *args, **kwargs):
        np_bytes= self.enc_func(self.image)
        np_base64 = base64.b64encode(np_bytes)
        self.image_encoding = np_base64
        return super(register, self).save()


    image_encoding = models.BinaryField()

    @property
    def base64_to_numpy(self):
        np_bytes = base64.b64decode(self.image_encoding)
        return pickle.loads(np_bytes)

    def __str__(self):
        return self.name
    