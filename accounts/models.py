from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from .managers import UserManager
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser, PermissionsMixin):
    username = models.CharField(max_length=65, unique=True)
    email = models.EmailField(max_length=250, unique=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.email
    
    @property
    def is_staff(self):
        return self.is_admin
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    fullname = models.CharField(max_length=60, null=True, blank=True)
    age = models.PositiveSmallIntegerField(default=0)
    bio = models.TextField(null=True, blank=True)
    picture = models.ImageField(upload_to='profile_images', null=True, blank=True)

    
def create_profile(sender, **kwargs):
    if kwargs['created']:
        Profile.objects.create(user=kwargs['instance'])

post_save.connect(receiver=create_profile, sender=User)