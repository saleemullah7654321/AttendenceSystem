from django.db import models
# Create your models here.
class register(models.Model):
    emp_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=30)
    image = models.ImageField(upload_to='images', default="")

    def __str__(self):
        return self.name
    
