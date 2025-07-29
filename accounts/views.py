from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.views import View
from accounts.forms import RegisterForm
from accounts.mixins import SkipIfAuthenticatedMixin

# Create your views here.
class LoginView(SkipIfAuthenticatedMixin, View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'accounts/login.html', {'form': form})

    def post(self, request):
        """If there is an attempt to crawl the form through a direct POST request, we will have to reject it"""

        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')

        return render(request, 'accounts/login.html', {'form': form})

class RegisterView(SkipIfAuthenticatedMixin, View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

        return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile_view(request):
    user = User.objects.get(id=request.user.id)

    return render(request, 'accounts/profile.html', {'user': user})

@login_required
def logout_view(request):
    logout(request)

    return redirect('/')
