from django.shortcuts import render, redirect
from .models import Program
from .forms import NewProgramForm
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

# Create your views here.
class ProgramPageView():
    def __init__(self):
        self.form = NewProgramForm()
        self.model = Program
    
    def as_view(self, request):
        print(request.method)
        if request.method == "GET":
            return(render(request, 'programs/main.html', {'programs': Program.objects.all()}))
        elif request.method == "POST":
            if 'add' in request.POST:
                return(render(request, 'programs/new_program.html'))
                print(request.POST)
            elif 'add_program' in request.POST:
                valid, program_id = self.form.is_valid(request)
                if valid:
                    return HttpResponseRedirect(reverse('program_details', 
                kwargs={'program_id':program_id}))
                else:
                    return(render(request, 'programs/new_program.html'))


class ProgramDetailsView():       
    def as_view(self, request, program_id):
        self.program = Program.objects.filter(program_id=program_id).first()
        if request.method == 'GET':
            return(render(request, 'programs/details.html', {'program': self.program}))
        if request.method == 'POST':
            if 'completed' in request.POST:
                if (request.user == task.executor or request.user == task.head):
                    task.status = 'Complete'
                    task.save(update_fields = ['status'])
                return(render(request, 'daily_tasks/details.html', {'task': task, 
                'days': days, 'hours': hours}))
            elif 'in_progress' in request.POST:
                task.status = 'In progress'
                task.save(update_fields = ['status'])
                return(render(request, 'daily_tasks/details.html', {'task': task, 
                'days': days, 'hours': hours}))
            elif 'delete' in request.POST:
                task.delete()
                return redirect('tasks:tasks_page')

def calculate_time(task):
    time_left = (task.end_date - timezone.now()).total_seconds()
    if time_left > 0:
        days_left = int(time_left//(24*3600))
        hours_left = int(time_left - days_left*(24*3600))//3600
    else:
        days_left = hours_left = 0
    return (days_left, hours_left)

    