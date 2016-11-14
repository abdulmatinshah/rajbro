from django.shortcuts import render
from django.views.generic import ListView
from .models import Customer


class Customer(ListView):
    model = Customer
