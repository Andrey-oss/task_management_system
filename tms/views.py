from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from tms.forms import TaskForm
from tms.models import Task
from crypter.handle_text import HandleText

# Create your views here.

class LoginRequired(LoginRequiredMixin):
    login_url = 'login'
    redirect_field_name = 'next'

class CreateTask(LoginRequired, View):
    def get(self, request):
        form = TaskForm()
        return render(request, 'tasks/credit_task.html', {'form': form, 'is_new': True})

    def post(self, request):
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            task = form.save(commit=False)
            task.author = request.user
            passwd = form.cleaned_data.get('password')

            if passwd:
                enc = HandleText(password=passwd)
                task.text = enc.encrypt(plaintext=task.text)

            task.save()
            return redirect('my_tasks')

        return render(request, 'tasks/credit_task.html', {'form': form})

class ReadTask(LoginRequired, View):
    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        return render(request, 'tasks/read_task.html', {'task': task})

    def post(self, request, pk):
        '''If task contains password, decode data and send it via GET'''

        password = request.POST.get('password')
        task = get_object_or_404(Task, pk=pk)

        if task.password == password:
            dec = HandleText(password=password)
            task.text = dec.decrypt(task.text)
            task.password = None
            return render(request, 'tasks/read_task.html', {'task': task})

        return render(request, 'tasks/read_task.html', {'task': task})

class UpdateTask(LoginRequired, View):
    html_template = 'tasks/credit_task.html'

    def get(self, request, pk):
        if request.user.is_superuser:
            task = get_object_or_404(Task, pk=pk)
        else:
            task = get_object_or_404(Task, pk=pk, author=request.user)

        form = TaskForm(instance=task)

        return render(request, self.html_template, {
            'form': form,
            'is_new': False,
            'task_password': task.password
        })

    def post(self, request, pk):
        if request.user.is_superuser:
            task = get_object_or_404(Task, pk=pk)
        else:
            task = get_object_or_404(Task, pk=pk, author=request.user)

        if task.password:
            password = request.POST.get('password')
            encrypted = request.POST.get('encrypted') == 'true'

            if task.password == password and encrypted:
                dec = HandleText(password=password)
                task.text = dec.decrypt(task.text)
                form = TaskForm(instance=task)
                return render(request, self.html_template, {
                    'form': form,
                    'is_new': False,
                    'task_password': False
                })

        form = TaskForm(request.POST, request.FILES, instance=task)

        if form.is_valid():
            task = form.save(commit=False)
            task.author = request.user
            passwd = form.cleaned_data.get('password')

            if passwd:
                enc = HandleText(password=passwd)
                task.text = enc.encrypt(plaintext=task.text)

            task.save()
            return redirect('my_tasks')

        return render(request, self.html_template, {
            'form': form,
            'is_new': False,
            'task_password': task.password
        })

class DeleteTask(LoginRequired, View):
    def get(self, request, pk):
        task = Task.objects.get(pk=pk)
        return render(request, 'tasks/delete_task.html', {'task': task})

    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        task.delete()

        return redirect('my_tasks')

class DisplayMyTasks(LoginRequired, View):
    def get(self, request):
        if request.user.is_superuser:
            tasks = Task.objects.all()
        else:
            tasks = Task.objects.filter(author=request.user)

        filter_value = request.GET.get('filter', 'all') # Default value - all

        if filter_value == 'all':
            filtered_tasks = tasks.filter()

        else:
            filtered_tasks = tasks.filter(status=filter_value.upper())

        return render(request, 'tasks/my_tasks.html', {'tasks': filtered_tasks})
