from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.views import generic
from products.models import Product
from .forms import ContactForm

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