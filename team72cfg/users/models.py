from django.db import models
from django.contrib.auth.models import User
from phone_field import PhoneField
#from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    image=models.ImageField(default='default.jpg',upload_to='profile_pics')
    phone = models.CharField(max_length=12)
    def __str__(self):
        return f'{self.user.username} Profile'