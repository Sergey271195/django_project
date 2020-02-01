from django.shortcuts import render, redirect
from .models import Program
from .forms import NewProgramForm, UpdateProgramForm, SortProgramsForm
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone

# Create your views here.
class ProgramPageView():
    def __init__(self):
        self.form = NewProgramForm()
        self.sort_form = SortProgramsForm()
        self.model = Program
    
    def as_view(self, request):
        print(request.method)
        if request.method == "GET":
            for program in Program.objects.all():
                program.in_current_status = update_status_time(program)
                program.save(update_fields = ['in_current_status'])
            return(render(request, 'programs/main.html', {'programs': Program.objects.all()}))
        elif request.method == "POST":
            if 'add' in request.POST:
                return(render(request, 'programs/new_program.html'))
            elif 'add_program' in request.POST:
                valid, program_id = self.form.is_valid(request)
                if valid:
                    return(redirect('programs_page'))
                else:
                    return(render(request, 'programs/new_program.html'))
            elif 'sort' in request.POST:

                print(request.POST)
                print(request.POST.keys())
                print(len(request.POST.keys()))
                content = self.sort_form.sort_programs(request)

                return(render(request, 'programs/main.html', {'programs': content}))

        


class ProgramDetailsView():
    def __init__(self):
        self.form = UpdateProgramForm()

    def as_view(self, request, program_id):
        self.program = Program.objects.filter(program_id=program_id).first()
        if request.method == 'GET':
            if self.program is not None:
                return(render(request, 'programs/details.html', {'program': self.program}))
            else:
                return(redirect('programs_page'))

        if request.method == 'POST':
            if 'delete_program' in request.POST:
                self.program.delete()
                return(redirect('programs_page'))
            elif 'update_program' in request.POST:
                self.form.is_valid(request, self.program)
                return(redirect('programs_page'))

def update_status_time(program):
    time_passed = (timezone.now()-program.status_update).total_seconds()
    days_passed = int(time_passed//(24*3600))
    return (days_passed)

    