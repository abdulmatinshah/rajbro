from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse_lazy

from django.views import generic
from braces import views as bv

from products.models import Product
from .forms import ContactForm, LoginForm

from .forms import RegistrationForm, AuthenticationForm
class DashboardView(generic.View):

    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        form = ContactForm(request.POST or None)
        context = {
            'form': form,
            "products": products,
        }
        return render(request, 'dashboard/view.html', context)

    def post(self, request, *args, **kwargs):

        form = ContactForm(request.POST)
        if form.is_valid():
            subject = 'Message Subject'
            msg = 'Message:{}'.format(form.cleaned_data.get('message'))
            from_whom = '{name}<{email}>Ph:{phone}'.format(**form.cleaned_data)
            to_whom = ['cp12344@yahoo.com', ]
            send_mail(subject, msg, from_whom, to_whom)
            messages.success('Message email sent!')
            context = {}
            return render(request, 'dashboard/back.html', context)
        else:
            print('post')
            context = {
                'form': form,
            }
            return render(request, 'dashboard/view.html', context)
        return HttpResponseRedirect(request.GET.get('next', '/'))


class RegisterView(
    bv.AnonymousRequiredMixin,
    bv.FormValidMessageMixin,
    generic.CreateView
):
    form_class = RegistrationForm
    form_valid_message = "You've been successfully registered"
    model = User
    template_name = 'dashboard/register.html'


class LoginView(
    bv.AnonymousRequiredMixin,
    bv.FormValidMessageMixin,
    generic.FormView
):
    form_class = LoginForm
    form_valid_message = "You've been successfully logged in"

    success_url = reverse_lazy('dashboard')
    template_name = 'dashboard/login.html'

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        user = authenticate(username=username, password=password)
        if user is not None and user.is_active():
            login(self.request, user)
            return super().form_valid(form)
        else:
            return super().form_invalid(form)


class LogoutView(bv.LoginRequiredMixin, generic.RedirectView):
    url = reverse_lazy('home')
