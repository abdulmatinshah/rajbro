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
    class Meta:
        model = LineItem
        fields = ['product', 'quantity', 'subtotal','quantity_returned']

    # def clean(self):
        # cleaned_data = super().clean()
        # print(cleaned_data.get('quantity'), 'from cleaned data', type(cleaned_data))
        # if cleaned_data.get('quantity') is None:
        #    p = cleaned_data.pop('product')
        #    cleaned_data.update({'product': {'value': None}})
        # q= self['quantity'].value()
        # if not q:
        #     print(cleaned_data.get('product'))
        #
        #     print('---------------------------', q, p)
        # return cleaned_data




LineItemFormSet = forms.modelformset_factory(
    LineItem,
    form=LineItemForm,
)

LineItemInlineFormSet = forms.inlineformset_factory(
    PurchaseOrder,
    LineItem,
    form=LineItemForm,
    # formset=LineItemFormSet,
    fields=['product', 'quantity', 'subtotal', 'quantity_returned'],
    # can_delete=True,
    # can_order=True,
    extra=1,
    # min_num=Product.objects.count(),
)
