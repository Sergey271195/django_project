from django import forms
from .models import Program
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime


# Create your models here.

class NewProgramForm(forms.ModelForm):
    def __init__(self):
        self.model = Program()
        self.create_dict = {}

    def check_id_kks(self):
        if (Program.objects.filter(program_id = self.ID).first() is None and
            Program.objects.filter(KKS= self.KKS).first() is None):
            return True
        else:
            return False
        
    def is_valid(self, request):
        if request.method == 'POST':
            print(request.POST)

            self.model = Program()
            self.ID = request.POST['program_id']
            self.KKS = request.POST['KKS']
            
            if self.check_id_kks():
                for field in request.POST:
                    if field != 'csrfmiddlewaretoken':
                        setattr(self.model, field, request.POST[field])
                self.model.save()
                return (True, self.model.program_id)
            else:
                return(False, None)


class UpdateProgramForm(forms.ModelForm):
    def __init__(self):
        self.model = Program()
        self.update_dict = {}

    def check_id_kks(self):
        if ('ID' in self.update_dict and 'KKS' in self.update_dict):
            if (Program.objects.filter(program_id = self.update_dict['ID']).first() is None and
                Program.objects.filter(KKS= self.update_dict['KKS']).first() is None):
                return True
            else:
                return False
        elif 'ID' in self.update_dict:
            if Program.objects.filter(program_id = self.update_dict['ID']).first() is None:
                return True
            else:
                return False
        elif 'KKS' in self.update_dict:
            if Program.objects.filter(KKS = self.update_dict['KKS']).first() is None:
                return True
            else:
                return False
        else:
            return True
        
    def is_valid(self, request, program):
        for field in request.POST:
            if (request.POST[field] != '' and field != 'csrfmiddlewaretoken'):
                self.update_dict[field] = request.POST[field]

        if self.check_id_kks():
            if ('status' in self.update_dict and program.status != self.update_dict['status']):
                program.status_update = timezone.now()
                program.save(update_fields = ['status_update'])
            for field in self.update_dict:
                setattr(program, field, self.update_dict[field])
                program.save(update_fields = [field])

            program.last_modified = timezone.now()
            program.modified_by = request.user
            program.save(update_fields = ['last_modified', 'modified_by'])

            
                
        