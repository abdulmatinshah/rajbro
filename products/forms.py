from re import split
import re

from django import forms
from .models import Product


def update_units(form, obj):
    new_stock = obj.units_in_stock
    box_units = form.cleaned_data['boxes']
    boxes, pieces = 0, 0
    if box_units:
        if ',' not in box_units:
            boxes += int(box_units)
        else:
            boxes, pieces = map(int, split(',', box_units))
        if boxes >= 0:
            if pieces > obj.quantity_per_unit:
                b, p = divmod(pieces, obj.quantity_per_unit)
                boxes += b
                pieces = p
            # print('boxes: %s   -   pieces: %s' % (boxes, pieces))
            new_qty = boxes * obj.quantity_per_unit + pieces
            new_stock = obj.units_in_stock + new_qty
            # print('------',boxes,'-------new', new_qty,'------sotck', obj.units_in_stock, '----new stok', new_stock)
        else:
            boxes *= -1
            if pieces > obj.quantity_per_unit:
                b, p = divmod(pieces, obj.quantity_per_unit)
                boxes += b
                pieces = p
            # print('boxes: %s   -   pieces: %s' % (boxes, pieces))
            new_qty = boxes * obj.quantity_per_unit + pieces
            new_stock = obj.units_in_stock - new_qty
            # print('------', boxes, '-------new', new_qty, '------sotck', obj.units_in_stock, '----new stok', new_stock)
    if new_stock:
        obj.units_in_stock = new_stock
    return obj


class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['units_in_stock'].widget.attrs['readonly'] = True
            self.fields['boxes'].widget.attrs['readonly'] = True

    boxes = forms.CharField(max_length=20, help_text='boxes,pieces - Please follow format', required=False,widget=forms.TextInput(attrs={'placeholder': '0,0'}))


    class Meta:
        model = Product
        exclude = []

    def clean_boxes(self):
        value = self.cleaned_data['boxes']
        if value is not None:
            return value
        pattern = re.compile("^\d+,\d+$")
        result = pattern.match(value)
        if not result:
            raise forms.ValidationError("Your value must be in boxes,pieces format")
        return value
    #
    # def save(self, commit=True):
    #     obj = super().save(commit=False)
    #     update_units(self, obj)
    #     obj.save()
    #     return obj


# ============ MODELFORMSET =========

ProductFormSet = forms.modelformset_factory(
   Product,
   fields=['name', 'weight', 'quantity_per_unit', 'purchase_rate', 'sale_rate', 'discontinued'],
   extra=1,
)