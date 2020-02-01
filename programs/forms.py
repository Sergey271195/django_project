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


class SortProgramsForm(forms.ModelForm):
    sorted = False
    def __init__(self):
        self.model = Program
        self.all_programs = self.model.objects.all()
        self.sort_dict = ['Type', 'Block', 'Status', 'Updated', 'Curr_status']
        self.order_dict = ['id', 'name', 'Updated_order', 'Curr_status_order']
        self.searched = False
        '''self.sorted = False
        self.content = self.all_programs'''

    def valid_sort(self, request):
        if (len(request.POST.keys()) > 2 and ~self.sorted):
            self.content = self.model.objects
        elif self.sorted:
            pass
        else:
            self.content = self.model.objects.all()

    def order(self, request, order_fields):
        self.order_tuple = tuple()
        for field in order_fields:
            if field == 'id':
                if request.POST[field] == 'Descending':
                    self.order_tuple += ('-program_id',)
                else:
                    self.order_tuple += ('program_id',)
            elif field == 'name':
                if request.POST[field] == 'Z-A':
                    self.order_tuple += ('-'+field,)
                else:
                    self.order_tuple += (field,)
            elif field == 'Updated_order':
                if request.POST[field] == 'Old':
                    self.order_tuple += ('-last_modified',)
                else:
                    self.order_tuple += ('last_modified',)
            elif field == 'Curr_status_order':
                if request.POST[field] == 'Old':
                    self.order_tuple += ('-status_update',)
                else:
                    self.order_tuple += ('status_update',)
        self.content = self.content.order_by(*self.order_tuple)

    def sort(self, request, sort_fields):
        self.type_fields = ['PMO', 'GI', 'PNR', 'IE']
        self.sort_dict = {}
        self.sort_dict = ['Type', 'Block', 'Status', 'Updated', 'Curr_status']
        '''last_modified = models.DateTimeField(default = timezone.now)
        status_update = models.DateTimeField(default = timezone.now)
        program_id = models.IntegerField()
        KKS = models.CharField(max_length = 20)
        name = models.TextField()
        status = models.CharField(max_length = 20)
        details = models.TextField()
        program_type = models.CharField(max_length = 20)
        block = models.IntegerField()
        in_current_status = 1'''
        if self.sorted:
            self.content = self.model.objects

        for field in sort_fields:
            if field == 'Type':
                for program_type in self.type_fields:
                    if program_type not in request.POST.getlist(field):
                        self.content = self.content.exclude(program_type = program_type)
                self.sorted = True



           


        
    def sort_programs(self, request):
        if ~self.searched:
            self.curr_order_dict = []
            self.curr_sort_dict = []
            self.valid_sort(request)
            for field in request.POST:
                if field in self.order_dict:
                    self.curr_order_dict.append(field)
                elif field in self.sort_dict:
                    self.curr_sort_dict.append(field)
            self.sort(request, self.curr_sort_dict)
            self.order(request, self.curr_order_dict)
            return self.content
        else:
            return self.content


            if self.searched:
                if self.request.POST['filter_choice'] in self.filter_requests[0:2]:
                    self.content = self.searched_content.filter(status = self.request.POST['filter_choice'])
            else:
                if self.request.POST['filter_choice'] in self.filter_requests[0:2]:
                    self.content = self.searched_content.filter(status = self.request.POST['filter_choice'])
                else:
                    self.content = self.model.objects.all()
        if not self.filtered:
            self.searched_content = self.content
            self.filtered = True
            if self.searched:
                if self.request.POST['filter_choice'] in self.filter_requests[0:2]:
                    self.content = self.searched_content.filter(status = self.request.POST['filter_choice'])
            else:
                if self.request.POST['filter_choice'] in self.filter_requests[0:2]:
                    self.content = self.content.filter(status = self.request.POST['filter_choice'])
                else:
                    self.content = self.model.objects.all()



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

            
                
        