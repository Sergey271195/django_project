from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Task
from django.urls import reverse
from .forms import NewTaskForm
from django.contrib.auth.models import User


# Create your views here.

class TaskPageView():
    def __init__(self):
        self.model = Task
        self.user_model = User
        self.post_requests = ['completed', 'details', 'create_task', 'search_button']
        self.search_requests = ['executor', 'head', 'content', 'assignment_date']
        self.content = self.model.objects.all()
        self.arr = self.search_requests.copy()

    def filter_again(self):
        return True

    def search(self):
        #self.filter = self.request.POST.get('input_search')
        self.search_req = [search for search in self.search_requests][0]
        self.arr.pop(self.search_req)
        self.filter = self.request.POST.get(self.search_req)
        if self.search_req == 'content':
            self.content = self.model.objects.filter(content__icontains = self.filter)
            #return self.model.objects.filter(executor = self.filter)
        if self.search_req == 'executor':
            filt_user = User.objects.filter(username__icontains = self.filter).first()
            if filt_user is not None:
                self.content = self.model.objects.filter(executor_id = filt_user.id)
        if self.request.POST['search'] == 'head':
            filt_user = User.objects.filter(username__icontains = self.filter).first()
            if filt_user is not None:
                self.content = self.model.objects.filter(head_id = filt_user.id)  
    
    def search_1(self):
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
        print(self.request.POST)
        if self.post_requests[2] in self.request.POST:
            self.form = NewTaskForm()
            self.form.is_valid(self.request)
            return redirect('tasks:tasks_page')
        elif self.post_requests[0] in self.request.POST:
            self.pk = self.request.POST.get(self.post_requests[0])
            self.task = Task.objects.filter(pk=self.pk).first()
            self.task.status = 'Complete'
            self.task.save(update_fields = ['status'])
            return redirect('tasks:tasks_page')
        elif self.post_requests[1] in self.request.POST:
            return HttpResponseRedirect(reverse('tasks:task_details', kwargs={'pk':self.request.POST.get(self.post_requests[1])}))
        elif self.post_requests[3] in self.request.POST:
            self.search_1()
            return(render(self.request, 'daily_tasks/home.html', {'tasks':self.content}))
        else:
            return(render(self.request, 'daily_tasks/home.html', {'tasks':self.content}))

def task_details(request, pk):
    return(render(request, 'daily_tasks/details.html', {'task': Task.objects.filter(pk=pk).first()}))

def tasks_page_about(request):
    content = {
        "title": "About"
    }
    return(render(request, 'daily_tasks/about.html', content))