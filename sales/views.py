from functools import reduce
from heapq import merge
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.views.generic import ListView
from .models import Sale, SaleLineItem
from .forms import SaleForm, ItemInlineFormSet, TestItemForm, DailySaleFormSet
from django.contrib import messages


class SaleOrders(ListView):
    model = Sale
    paginate_by = 10


class SaleByCustomer(ListView):
    model = Sale
    ordering = ['customer']
    template_name = 'sales/sale_by_customer.html'


class SaleByDate(ListView):
    model = Sale
    ordering = ['sale_date']
    template_name = 'sales/sale_by_date.html'


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
                raise ValueError('Incorrect value')
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


from django.db.models import Sum
from datetime import date, datetime


def invoice(request, year=None, month=None, day=None):
    d=''
    if request.method == 'POST':
        d = request.POST['d']
        if d:
            asked_day = datetime.strptime(d,'%Y/%m/%d')
        else:
            asked_day = date.today()
    else:
        # inv = Sale.objects.filter(sale_date__month=11)
        if year and month and day:
            asked_day = date(int(year), int(month), int(day))
        else:
            asked_day = date.today()
    inv = Sale.objects.filter(sale_date=asked_day)

    context = {
        'invoice': inv,
        'asked_day': asked_day,
        'd': d,
    }

    return render(request, 'sales/invoice.html', context)

'''
def gatepass(request, year=None, month=None, day=None):
    # from datetime import date, datetime
    # d=''
    # if request.method == 'POST':
    #     d = request.POST['d']
    #     if d:
    #         asked_day = datetime.strptime(d,'%Y/%m/%d')
    #     else:
    #         asked_day = date.today()
    # else:
    #     # gpass = Sale.objects.filter(sale_date__month=11)
    #     if year and month and day:
    #         asked_day = date(int(year), int(month), int(day))
    #     else:
    #         asked_day = date.today()
    # gpass = Sale.objects.filter(sale_date=asked_day)

   from django.db.models.query import Q
    Post.objects.filter(Q(parent = post) | Q(parent__parent = post))
    Publisher.objects.all().prefetch_related('book_set', 'book_set__page_set')
    from django.db.models.query import Q



    dsr = request.user
    # r = dsr.sales.sale_line_items.all()
    r = dsr.sales.prefetch_related('sale_line_items')

    from django.db.models import Sum
    # r = Sale.objects.annotate(i=Sum('sale_line_items__quantity'))
    r = Sale.objects.all().values('sale_line_items__product__name').annotate(s=Sum('sale_line_items__quantity'))
    Cheetos: 4
    Kurkray: 23
    Lays 9: 19
    Cheetos: 4
    Kararay: 4
    Lays 9: 15

    yesterday = (date.today() - timedelta(1))
    dsr_id='0'
    asked_day = date.today()
    print('iso format', asked_day)

    sale_reps = User.objects.all().exclude(is_superuser=True)

    r = Sale.objects.filter(sale_date=asked_day).values('sale_line_items__product__name', 'sale_line_items__product__quantity_per_unit').annotate(
        s=Sum('sale_line_items__quantity'))
    # gpass = Sale.objects.filter(sale_date=date.today()).values('sale_line_items__product__name', 'sale_line_items__product__quantity_per_unit').annotate(s=Sum('sale_line_items__quantity'))
    gpass = Sale.objects.filter(sale_date=asked_day).values('sale_line_items__product__name', 'sale_line_items__product__quantity_per_unit').annotate(s=Sum('sale_line_items__quantity'))

    if request.method == 'POST':
        asked_day = request.POST.get('asked_day')
        asked_day = datetime.strptime(asked_day, '%Y-%m-%d')

        print(asked_day)
        dsr_id = request.POST.get('dsr')
        if dsr_id=='0':
            r = Sale.objects.filter(sale_date=asked_day).values('sale_line_items__product__name', 'sale_line_items__product__quantity_per_unit').annotate(s=Sum('sale_line_items__quantity'))
        else:
            r = Sale.objects.filter(sale_date=asked_day, sales_rep=dsr_id).values('sale_line_items__product__name', 'sale_line_items__product__quantity_per_unit').annotate(
                s=Sum('sale_line_items__quantity'))

    from collections import defaultdict
    c = defaultdict(int)
    for d in r:
        c[d['sale_line_items__product__name'], d['sale_line_items__product__quantity_per_unit']] += d['s']

    print(c)


    r = [{'item': item, 'amount': amount} for item, amount in c.items()]
    context = {
        'gpass': gpass,
        'r': r,
        'sale_reps': sale_reps,
        'dsr_id': dsr_id,
        'asked_day': asked_day.strftime('%Y-%m-%d'),
    }

    return render(request, 'sales/gatepass.html', context)
'''

def gatepass(request):
    asked_day = date.today()
    dsr_id = '0'
    sale_reps = User.objects.all().exclude(is_superuser=True)

    day_sale = Sale.objects.filter(sale_date=asked_day)
    gatepass = User.objects.filter(sale__in=day_sale)\
        .order_by('username')\
        .values('username',
                'sale__sale_line_items__product__name',
                'sale__sale_line_items__product__quantity_per_unit') \
        .annotate(total=Sum('sale__sale_line_items__quantity'))


    if request.method == 'POST':
        # http: // stackoverflow.com / questions / 28417613 / django - filter - queryset - with-child - objects - foreignkey
        asked_day = request.POST.get('asked_day')
        asked_day = datetime.strptime(asked_day, '%Y-%m-%d')
        day_sale = Sale.objects.filter(sale_date=asked_day)

        dsr_id = request.POST.get('dsr')
        if dsr_id == '0':
            gatepass = User.objects \
                .filter(sale__in=day_sale)\
                .order_by('username') \
                .values('username',
                        'sale__sale_line_items__product__name',
                        'sale__sale_line_items__product__quantity_per_unit')\
                .annotate(total=Sum('sale__sale_line_items__quantity'))
        else:
            gatepass = User.objects \
                .filter(id=dsr_id) \
                .filter(sale__in=day_sale) \
                .values('username',
                        'sale__sale_line_items__product__name',
                        'sale__sale_line_items__product__quantity_per_unit') \
                .annotate(total=Sum('sale__sale_line_items__quantity'))
    context = {
        'gatepass': gatepass,
        'sale_reps': sale_reps,
        'dsr_id': dsr_id,
        'asked_day': asked_day.strftime('%Y-%m-%d'),
        'day': asked_day,
    }

    return render(request, 'sales/gatepass.html', context)

'''
def gatepass(request, year=None, month=None, day=None):


    yesterday = (date.today() - timedelta(1))
    dsr_id='0'
    asked_day = date.today()


    sale_reps = User.objects.all().exclude(is_superuser=True)

    r = Sale.objects.filter(sale_date=asked_day).values('sale_line_items__product__name', 'sale_line_items__product__quantity_per_unit').annotate(
        s=Sum('sale_line_items__quantity'))
    # gpass = Sale.objects.filter(sale_date=date.today()).values('sale_line_items__product__name', 'sale_line_items__product__quantity_per_unit').annotate(s=Sum('sale_line_items__quantity'))
    gpass = Sale.objects.filter(sale_date=asked_day).values('sale_line_items__product__name', 'sale_line_items__product__quantity_per_unit').annotate(s=Sum('sale_line_items__quantity'))

    if request.method == 'POST':
        asked_day = request.POST.get('asked_day')
        asked_day = datetime.strptime(asked_day, '%Y-%m-%d')

        print(asked_day)
        dsr_id = request.POST.get('dsr')
        if dsr_id=='0':
            r = Sale.objects.filter(sale_date=asked_day).values('sale_line_items__product__name', 'sale_line_items__product__quantity_per_unit').annotate(s=Sum('sale_line_items__quantity'))
        else:
            r = Sale.objects.filter(sale_date=asked_day, sales_rep=dsr_id).values('sale_line_items__product__name', 'sale_line_items__product__quantity_per_unit').annotate(
                s=Sum('sale_line_items__quantity'))

    from collections import defaultdict
    c = defaultdict(int)
    for d in r:
        c[d['sale_line_items__product__name'], d['sale_line_items__product__quantity_per_unit']] += d['s']

    print(c)


    r = [{'item': item, 'amount': amount} for item, amount in c.items()]
    context = {
        'gpass': gpass,
        'r': r,
        'sale_reps': sale_reps,
        'dsr_id': dsr_id,
        'asked_day': asked_day.strftime('%Y-%m-%d'),
    }

    return render(request, 'sales/gatepass.html', context)
'''
def testgatepass(request):
    dsr = request.user
    # s = Sale.objects.prefetch_related('')
    # gpass = dsr.sale_set.prefetch_related('sale_line_items')
    # gpass = User.objects.all().prefetch_related('sale_set', 'sale_set__sale_line_items').annotate(u=Sum('sale__sale_line_items__linetotal'))
    # gpass = User.objects.all().annotate(s=Sum('sale_set__sale_line_items__line'))
    # print(gpass.query)
    result = User.objects.order_by('username').values('username', 'sale__sale_line_items__product__name', 'sale__sale_line_items__product__quantity_per_unit').annotate(s=Sum('sale__sale_line_items__quantity'))

    context = {
        'result': result,
    }
    return render(request, 'sales/testgatepass.html', context)
