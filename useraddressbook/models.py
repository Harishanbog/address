from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.shortcuts import reverse

# Create your models here.
class address(models.Model):
    user=models.ForeignKey(User,on_delete=CASCADE,blank=True,null=True)
    name=models.CharField(max_length=200)
    phone=models.BigIntegerField()
 

    def __str__(self):
        return f"{self.user.username} {self.name}"

    def get_delete_object(self):
        return reverse("useraddressbook:delete_address",kwargs={
            'slug':self.name
        })    

   