from .models import LineItem, PurchaseOrder
from django import forms


class PurchaseOrderForm(forms.ModelForm):

    class Meta:
        model = PurchaseOrder
        fields = ['post_items']
        labels = {
            'post_items': 'Post items to inventory',
        }

class LineItemForm(forms.ModelForm):
    to_box = forms.CharField(max_length=10, required=False, label='Boxes,Pieces')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance.posted:
            for k in self.fields:
                self.fields[k].widget.attrs['readonly'] = True
                # if k == 'product':
                #     self.fields[k].widget.attrs['disabled'] = True

        # self.fields['product'].widget.attrs['disabled'] = True
        # self.fields['product'].widget.attrs['required'] = False
        self.fields['subtotal'].widget.attrs['readonly'] = True
        if hasattr(instance, 'product'):
            self.fields['to_box'].widget.attrs['value'] = self.instance.to_box

    class Meta:
        model = LineItem
        fields = ['product', 'to_box', 'subtotal']

    def clean_to_box(self):
        boxes = self['to_box'].value()
        product = self['product'].value()
        self.instance.to_quantity_from_box(boxes, product)
        # else:
        #     self.instance.to_box_from_value(data)
        return boxes




LineItemFormSet = forms.modelformset_factory(
    LineItem,
    form=LineItemForm,
)

LineItemInlineFormSet = forms.inlineformset_factory(
    PurchaseOrder,
    LineItem,
    form=LineItemForm,
    # formset=LineItemFormSet,
    fields=['product', 'to_box','subtotal' ],
    # can_delete=True,
    # can_order=True,
    extra=1,
    # min_num=Product.objects.count(),
)
