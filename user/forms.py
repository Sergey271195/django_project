from django import forms
from django.contrib.auth.models import User
from .models import Profile
from django.core.validators import validate_email
import os


# Create your models here.
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

class UpdateUser(forms.ModelForm):

    def __init__(self):
        self.BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.model = User
        self.profile_model = Profile
        self.valid_email = False
        
    def is_valid(self, request):
        if request.method == 'POST':
            self.email = request.POST.get('email')
            if 'user_image' in request.FILES:
                filename = request.FILES['user_image'].name
                full_filename = os.path.join(self.BASE_DIR, 'media', 'profile_pics', filename)
                fout = open(full_filename, 'wb+')
                fout.write(request.FILES['user_image'].read())
                fout.close()
                request.user.profile.image = os.path.join('profile_pics', filename)
                request.user.profile.save()
            if self.email != '':
                try:
                    validate_email(self.email)
                    self.valid_email = True
                except validate_email.ValidationError:
                    self.valid_email = False
                if self.valid_email:
                    request.user.email = self.email
                    request.user.save()