from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponseRedirect
from .forms import LoginForm


def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request, u'Invalid credentials')
        if user.is_active:
            login(request, user)
            messages.error(request, u'Successfully logged in.')
            return HttpResponseRedirect(request.GET.get('next', '/'))
        else:
            messages.error(request, u'User is not active.')
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)


@login_required
def logout_view(request):
    logout(request)
    messages.error(request, u'Successfully logged out.')
    return redirect('dashboard')
