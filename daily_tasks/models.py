from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import os
from PIL import Image



class Task(models.Model):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    full_filename = os.path.join('media', 'utility', 'arrow.png')
    head = models.ForeignKey(User, on_delete = models.CASCADE, unique = False)
    executor = models.ForeignKey(User, related_name = 'executor', on_delete= models.CASCADE, unique = False)
    assignment_date = models.DateTimeField(auto_now = True)
    end_date = models.DateTimeField(default = timezone.now)
    content = models.TextField()
    status = models.CharField(max_length = 20)


