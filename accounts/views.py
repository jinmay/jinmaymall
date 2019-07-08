from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from .forms import UserCreationForm


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {
        'form': form,
    })


class LoginView(LoginView):
    template_name = 'accounts/login.html'

login = LoginView.as_view()


class LogoutView(LogoutView):
    next_page = '/'

logout = LogoutView.as_view()