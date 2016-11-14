from .models import Customer
from django.contrib import admin
from .models import Supplier
from sales.models import Sale, SaleLineItem
from nested_inline.admin import NestedStackedInline, NestedModelAdmin


class ItemInline(NestedStackedInline):
    model = SaleLineItem
    extra = 0
    fk_name = 'sale_order'


class SaleInline(NestedStackedInline):
    model = Sale
    extra = 0
    fk_name = 'customer'
    inlines = [ItemInline, ]


class CustomerAdmin(NestedModelAdmin):
    model = Customer
    inlines = [SaleInline, ]


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Supplier)


