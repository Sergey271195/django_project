from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import os
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image

class Program(models.Model):
    modified_by = models.ForeignKey(User, on_delete = models.SET('Deleted'), 
    unique = False, default = 1)
    last_modified = models.DateTimeField(default = timezone.now)
    status_update = models.DateTimeField(default = timezone.now)
    program_id = models.IntegerField()
    KKS = models.CharField(max_length = 20)
    name = models.TextField()
    status = models.CharField(max_length = 20)
    details = models.TextField()
    program_type = models.CharField(max_length = 20)
    block = models.IntegerField()
    in_current_status = models.IntegerField(default = 0)

    def __str__(self):
        return (str(self.KKS)+ ' -  ID '+str(self.program_id))

    def change_status(self):
        pass


