from django.contrib import admin
from .models import PurchaseOrder, LineItem


class InlineLineItem(admin.TabularInline):
    model = LineItem
    extra = 0
    fields = ['product', 'quantity', 'subtotal', 'posted']
    readonly_fields = ['subtotal', 'posted']

    # def get_subtotal(self, obj):
    #     if obj.quantity:
    #         print('---0--', obj.subtotal)
    #         obj.subtotal = obj.quantity * obj.product.sale_rate
    #         # obj.save()
    #         print('-----', obj.subtotal)
    #     return obj.subtotal


class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ['purchase_date', 'id', 'amount', 'post_items']
    readonly_fields = ['amount', ]
    inlines = [InlineLineItem, ]

    # def save_model(self, request, obj, form, change):
    #     pass  # don't actually save the parent instance

    def save_formset(self, request, form, formset, change):
        formset.save()  # this will save the children
        form.instance.save()  # form.instance is the parent

admin.site.register(PurchaseOrder, PurchaseOrderAdmin)





