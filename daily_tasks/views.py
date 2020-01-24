from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Task
from django.urls import reverse
from .forms import NewTaskForm
from django.contrib.auth.models import User
from django.utils import timezone


# Create your views here.

class TaskPageView():
    def __init__(self):
        self.model = Task
        self.user_model = User
        self.post_requests = ['filter', 'details', 'create_task', 'search_button']
        self.search_requests = ['executor', 'head', 'content', 'assignment_date']
        self.filter_requests = ['Complete', 'In Progress', 'All']
        self.content = self.model.objects.all()
        self.arr = self.search_requests.copy()
        self.searched = False
        self.filtered  = False 

    def filter_again(self):
        return True

    def filter_button(self):
        if self.filtered:
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

    
    def search(self):
        self.searched = True
        self.filtered = False
        self.dict = {}
        if all(self.request.POST.get(filt) == '' for filt in self.search_requests):
            self.content = self.model.objects.all()
        else:
            for filt in self.search_requests:
                self.filter = self.request.POST.get(filt)
                if self.filter != '':
                    if filt in self.search_requests[0:2]:
                        filt_user = User.objects.filter(username__icontains = self.filter).first()
                        if filt_user is not None:
                            filt_param = filt_user.id
                            self.dict[filt] = filt_param
                    elif filt == self.search_requests[3]:
                        filt_param = self.filter
                        self.dict[filt+'__date'] = filt_param
                    else:
                        filt_param = self.filter
                        self.dict[filt+'__icontains'] = filt_param
            self.content = self.model.objects.filter(**self.dict)
        


    def as_view(self, request):
        self.request = request
        if self.post_requests[2] in self.request.POST:
            self.form = NewTaskForm()
            self.form.is_valid(self.request)
            return redirect('tasks:tasks_page')
        elif self.post_requests[0] in self.request.POST:
            if 'filter_choice' in self.request.POST:
                self.filter_button()
            return redirect('tasks:tasks_page')
        elif self.post_requests[1] in self.request.POST:
            return HttpResponseRedirect(reverse('tasks:task_details', kwargs={'pk':self.request.POST.get(self.post_requests[1])}))
        elif self.post_requests[3] in self.request.POST:
            self.search()
            return(render(self.request, 'daily_tasks/home.html', {'tasks':self.content.order_by('-assignment_date', '-end_date')}))
        else:
            return(render(self.request, 'daily_tasks/home.html', {'tasks':self.content.order_by('-assignment_date', '-end_date')}))

def calculate_time(task):
    time_left = (task.end_date - timezone.now()).total_seconds()
    if time_left > 0:
        days_left = int(time_left//(24*3600))
        hours_left = int(time_left - days_left*(24*3600))//3600
    else:
        days_left = hours_left = 0
    return (days_left, hours_left)

def task_details(request, pk):
    task = Task.objects.filter(pk=pk).first()
    days, hours = calculate_time(task)
    if request.method == 'GET':
        return(render(request, 'daily_tasks/details.html', {'task': task,
         'days': days, 'hours': hours}))
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
    

def tasks_page_about(request):
    content = {
        "title": "About"
    }
    return(render(request, 'daily_tasks/about.html', content))


class CreateTaskView():
    def __init__(self, *args):
        self.form  = NewTaskForm()
        self.user_model = User
        self.content = {'users': self.user_model.objects.all()}

    def as_view(self, request):
        if request.method == 'GET':
            return(render(request, 'daily_tasks/create.html', self.content))
        elif request.method == 'POST':
            return HttpResponseRedirect(reverse('tasks:task_details', 
                kwargs={'pk':self.form.is_valid(request)}))