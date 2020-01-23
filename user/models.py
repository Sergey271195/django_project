from django.db import models
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image

# Create your models here.
class MyUserForm(models.Model):
    def __init__(self, *args,**kwargs):
        self.model = User()
        self.already_exist_message = ""
        self.password_not_match_message = ""
        self.invalid_email = ""

    def password_check(self):
        if self.password_1 != self.password_2:
            self.password_not_match_message = "The two password fields didn't match."
            return(False)
        else:
            self.password_not_match_message = ""
            return(True)
    
    def email_check(self):
        if len(self.email) < 8:
            self.invalid_email = "Invalid email."
            return(False)
        else:
            #self.invalid_email = ""
            return(True)

    def username_check(self):
        username_list = list(user.get_username() for user in User.objects.all())
        if self.username in username_list:
            self.already_exist_message = "The account for this username already exists."
            return(False)
        else:
            self.already_exist_message  = ""
            return(True)
        
    def is_valid(self, request):
        if request.method == 'POST':
            self.username = request.POST.get('uname')
            self.password_1 = request.POST.get('psw1')
            self.password_2 = request.POST.get('psw2')
            self.email = request.POST.get('email')
            if all([self.password_check(),self.email_check(),self.username_check()]):
                try:
                    self.model.username = self.username
                    self.model.password = self.password_1
                    self.model.email = self.email
                    self.model.save()
                    messages.success(request, f'Successfully created account for {self.username}!')
                    login(request, self.model)
                    return(True)
                except IntegrityError as error:
                    self.already_exist_message = "The account for this username already exists."   
                
class LoginForm(models.Model):        
    def is_valid(self, request):
        if request.method == 'POST':
            self.username = request.POST.get('uname')
            self.password = request.POST.get('psw')
            user = authenticate(username = self.username, password = self.password)
            if user is not None:
                login(request, user)
                return(True) 

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    image = models.ImageField(default = "default.png", upload_to = 'profile_pics')

    def __str__(self):
        return(f'{self.user.username} Profile')

    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)

        img = Image.open(self.image.path)

        if img.height >300 or img.width >300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)

@receiver(post_save, sender = User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender = User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()