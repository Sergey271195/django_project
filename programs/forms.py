from django import forms
from .models import Program
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime


# Create your models here.

class NewProgramForm(forms.ModelForm):

    def __init__(self):
        self.model = Program()

    def check_id_kks(self):
        if (Program.objects.filter(program_id = self.ID).first() is None and
            Program.objects.filter(KKS= self.KKS).first() is None):
            return True
        else:
            return False
        
    def is_valid(self, request):
        if request.method == 'POST':
            self.ID = request.POST['ID']
            self.KKS = request.POST['KKS']
            self.program_type = request.POST['type']
            self.status = request.POST['status']
            self.block = request.POST['block']
            self.name = request.POST['name']
            self.details = request.POST['details']
            
            if self.check_id_kks():
                self.model.program_id = self.ID
                self.model.modified_by = User.objects.filter(username = request.user).first()
                self.model.last_modified = timezone.now()
                self.status_update = timezone.now()
                self.model.KKS = self.KKS
                self.model.name = self.name
                self.model.status = self.status
                self.model.deatils = self.details
                self.model.program_type = self.program_type
                self.model.block = self.block
                self.in_current_status = 0
                self.model.save()
                return (True, self.model.program_id)
            else:
                return(False, None)

