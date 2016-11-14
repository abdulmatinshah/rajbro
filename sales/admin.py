from django.contrib import admin
from .models import Sale, SaleLineItem


class InlineSaleLineItem(admin.TabularInline):
    model = SaleLineItem
    extra = 0
    fields = ['product', 'quantity', 'linetotal', 'posted']
    readonly_fields = ['linetotal', 'posted']


class SaleAdmin(admin.ModelAdmin):
    list_display = ['sale_date', 'id', 'amount', 'post_items']
    readonly_fields = ['amount', ]
    inlines = [InlineSaleLineItem, ]

    # def save_model(self, request, obj, form, change):
    #     pass  # don't actually save the parent instance

    def save_formset(self, request, form, formset, change):
        formset.save()  # this will save the children
        form.instance.save()  # form.instance is the parent

admin.site.register(Sale, SaleAdmin)

