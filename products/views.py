from django.shortcuts import render, redirect
from django.views.generic import ListView
from .models import Product
from .forms import ProductFormSet
from django.contrib import messages


class ProductList(ListView):
    model = Product


class ProductInventory(ListView):
    model = Product
    queryset = Product.objects.filter(discontinued=False)
    template_name = 'products/product_inventory.html'


def add_product(request):
    if request.method == 'POST':
        formset = ProductFormSet(request.POST)
        if formset.is_valid():
            formset.save()
        messages.success(request, 'Product updated successfully')
        return redirect('products:list')
    else:
        formset = ProductFormSet()

    context = {
        'formset': formset,
    }

    return render(request, 'products/product_form.html', context)