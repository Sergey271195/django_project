from django import forms
from .models import Task
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime


# Create your models here.

class NewTaskForm(forms.ModelForm):

    def __init__(self):
        self.model = Task()

    def check_user(self, executor):
        if User.objects.filter(username = executor).first() is None:
            return False
        else:
            return True

    def check_date(self, end_date):
        then = datetime.strptime(end_date, '%Y-%m-%d')
        delta = then - datetime.now()
        if delta.days >= 0:
            return True
        else:
            return False
        
    def is_valid(self, request):
        if request.method == 'POST':
            self.executor = request.POST.get('executor')
            self.end_date = request.POST.get('end_date')
            self.content = request.POST.get('content')
            
            if (self.check_user(self.executor) and self.check_date(self.end_date)):
                self.model.head = User.objects.filter(username = request.user).first()
                self.model.executor = User.objects.filter(username = self.executor).first()
                self.model.end_date = self.end_date
                self.model.content = self.content
                self.model.status = 'In Progress'
                self.model.save()