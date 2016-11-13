from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.views.generic import ListView
from .models import Sale, SaleLineItem
from .forms import SaleForm, ItemInlineFormSet, TestItemForm, DailySaleFormSet
from django.contrib import messages


class SaleOrder(ListView):
    model = Sale


def create_order(request, id=None):

    if id:
        so = get_object_or_404(Sale, pk=id)
        qs = so.sale_line_items.all()
    else:
        so = Sale(sales_rep=request.user)
        qs = so.sale_line_items.none()
    form = SaleForm(instance=so)
    formset = DailySaleFormSet(instance=so)

    if request.method == 'POST':

        form = SaleForm(request.POST, instance=so)
        formset = DailySaleFormSet(request.POST, instance=so)
        if form.is_valid():
            so = form.save(commit=False)
            if not so.id:
                so.save()
            # try:
            if formset.is_valid():
                items = formset.save(commit=False)
                total = 0
                for obj in formset.deleted_objects:
                    if obj.linetotal:
                        total -= obj.linetotal
                    obj.delete()

                for item in items:
                    item.save()
                    total += item.linetotal

                so.amount = total
                so.save()
            else:
                print('formset invalid')
                print(formset.errors)
            # except ObjectDoesNotExist:
            #     print('object does not exist', formset.errors)

            messages.success(request, 'Sale Entry made/updated successfully')
            return HttpResponseRedirect(so.get_absolute_url())
    context = {
        'form': form,
        'formset': formset,
    }
    return render(request, 'sales/create_order.html', context)


def test_form(request):
    so = Sale.objects.all().first()
    item = SaleLineItem.objects.all().first()
    form = SaleForm(instance=so)
    subform = TestItemForm(instance=item)

    if request.method == 'POST':
        form = SaleForm(request.POST, instance=so)
        subform = TestItemForm(request.POST,instance=item)
        if form.is_valid() and subform.is_valid():
            v = subform.cleaned_data['to_box']
            item.to_box = v
            print(item.quantity)
            print('both forms are valid', v)

    context = {
        'form': form,
        'subform': subform,
    }
    return render(request, 'sales/test_form.html', context)


def gatepass(request, year=None, month=None, day=None):
    from datetime import date, datetime
    d=''
    if request.method == 'POST':
        d = request.POST['d']
        if d:
            asked_day = datetime.strptime(d,'%Y/%m/%d')
        else:
            asked_day = date.today()
    else:
        # gpass = Sale.objects.filter(sale_date__month=11)
        if year and month and day:
            asked_day = date(int(year), int(month), int(day))
        else:
            asked_day = date.today()
    gpass = Sale.objects.filter(sale_date=asked_day)


    context ={
        'gpass': gpass,
        'asked_day': asked_day,
        'd': d,
    }

    return render(request, 'sales/gatepass.html', context)