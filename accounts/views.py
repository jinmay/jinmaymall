from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from .forms import UserCreationForm


def signup(request):
    if request.user.is_authenticated:
        return redirect('/')
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
    redirect_authenticated_user = True

login = LoginView.as_view()


@method_decorator(login_required, name='dispatch')
class LogoutView(LogoutView):
    next_page = '/'

logout = LogoutView.as_view()

@login_required
def mypage(request):
    user = request.user
    return render(request, 'accounts/mypage.html')
    