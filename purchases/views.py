from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, DeleteView

from braces import  views as bv

from .models import PurchaseOrder, LineItem
from .forms import PurchaseOrderForm, LineItemInlineFormSet


class Purchases(bv.LoginRequiredMixin, ListView):
    model = PurchaseOrder
    queryset = PurchaseOrder.objects.prefetch_related('line_items')


class PurchaseDetail(bv.LoginRequiredMixin, DetailView):
    model = PurchaseOrder


class PurchaseDelete(bv.LoginRequiredMixin, DeleteView):
    model = PurchaseOrder
    success_url = reverse_lazy('purchases:list')

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.post_items:
            messages.warning(request, 'This order is posted and items have been added to inventory. Unpost items and then you can deleting it.')
            return redirect('purchases:list')
        return super().get(request, *args, **kwargs)

@login_required
def purchase_order(request):
    form = PurchaseOrderForm()

    # data = []
    # from products.models import Product
    # products = Product.objects.all()
    # for p in products:
    #     data.append({'product': p})
    # print(data)
    # formset = LineItemInlineFormSet(initial=data)

    formset = LineItemInlineFormSet(queryset=LineItem.objects.none())
    if request.method == 'POST':
        form = PurchaseOrderForm(request.POST)
        formset = LineItemInlineFormSet(request.POST, queryset=LineItem.objects.none())

        if form.is_valid() and formset.is_valid():
            po = form.save()
            lineitems = formset.save(commit=False)
            total = 0
            for lineitem in lineitems:
                lineitem.purchase_order = po
                lineitem.save()
                total += lineitem.subtotal
            po.amount = total
            po.save()
            messages.success(request, 'Purchase order saved!')
            return redirect('purchases:list')
        else:
            messages.success(request, 'something went wrong')
            print(form.errors)
            print(formset.errors)
            for form in formset:
                print(form)

    context = {
        'form': form,
        'formset': formset,
    }
    return render(request, 'purchases/order_form.html', context)


@login_required
def edit_purchase_order(request, id):
    po = get_object_or_404(PurchaseOrder, pk=id)
    form = PurchaseOrderForm(instance=po)
    formset = LineItemInlineFormSet(instance=po)
    if request.method == 'POST':
        form = PurchaseOrderForm(request.POST, instance=po)
        formset = LineItemInlineFormSet(request.POST, instance=po)
        if form.is_valid() and formset.is_valid():
            po = form.save(commit=False)
            items = formset.save(commit=False)
            for item in formset.deleted_objects:
                item.delete()

            for item in items:
                item.purchase_order = po
                item.save()

            po.save()

        messages.success(request, 'Purchase order saved!')
        return redirect('purchases:list')
    context = {
        'form': form,
        'formset': formset,
    }
    return render(request, 'purchases/order_form.html', context)


@login_required
def post_items(request, id):
    po = get_object_or_404(PurchaseOrder, id=id)
    po.post_items = True
    po.save()
    messages.success(request, 'Order No. dated:{} costing Rs.{} posted to invenory'.format(po.id, po.purchase_date, po.amount))
    return redirect('purchases:list')


@login_required
def unpost_items(request, id):
    po = get_object_or_404(PurchaseOrder, id=id)
    po.post_items = False
    po.save()
    messages.success(request, 'Order No. {} dated:{} costing Rs.{} unposted from invenory'.format(po.id, po.purchase_date, po.amount))
    return redirect('purchases:list')


@login_required
def posting(request, posting_type):
    if posting_type =='post':
        messages.success(request, posting_type)
    else:
        messages.success(request, 'rest')
    return redirect('purchases:list')