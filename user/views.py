from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .models import MyUserForm
from .models import LoginForm
from django.contrib.auth import authenticate, login, logout
import re
from django.contrib.auth.models import User
from .forms import UserUpdateForm, ProfileUpdateForm, UpdateUser
# Create your views here.

def register(request):
    form = MyUserForm()
    if form.is_valid(request):
        return redirect('tasks:tasks_page')
    return render(request, 'user/register.html', {"form": form})


def login(request):
    form = LoginForm()
    if form.is_valid(request):
        return redirect('tasks:tasks_page')
    return render(request, 'user/login.html', {"form": form})

def logout_view(request):
    logout(request)
    return redirect('login')

def profile_view(request):
    form = UpdateUser()
    if form.is_valid(request):
        print('Hi')

    if request.user.is_authenticated:
        u_form = UserUpdateForm()
        p_form = ProfileUpdateForm()
        context = {
            'u_form': u_form,
            'p_form': p_form
        }
        return render(request, 'user/profile.html', context)
    else:
       return redirect('login') 



