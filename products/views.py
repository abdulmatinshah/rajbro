from django.shortcuts import render, redirect
from django.views.generic import ListView
from .models import Product
from .forms import ProductFormSet
from django.contrib import messages
from braces import views as bv
from django.contrib.auth.decorators import login_required

class ProductList(bv.LoginRequiredMixin, ListView):
    model = Product


class ProductInventory(bv.LoginRequiredMixin, ListView):
    model = Product
    queryset = Product.objects.filter(discontinued=False)
    template_name = 'products/product_inventory.html'


@login_required
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