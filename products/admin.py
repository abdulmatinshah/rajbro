from django.contrib import admin
from .models import Product
from .forms import ProductForm


class InlineProduct(admin.TabularInline):
    model = Product
    exclude = ['units_in_stock']
    extra = 0
    min_num = 1
    readonly_fields = ['units_in_stock']
    # form = ProductForm


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'boxes', 'discontinued', ]
    list_editable = ['discontinued']
    form = ProductForm

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # form.base_fields['boxes'].initial = obj.convert_unit
        return form

    # add_form_template = "admin/add_form.html"
    # change_form_template = "admin/change_form.html"

    def boxes(self, obj):
        return obj.box_units


admin.site.register(Product, ProductAdmin)



