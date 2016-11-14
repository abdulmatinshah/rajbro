from django import forms
from sales.models import SaleLineItem, Sale


class ItemForm(forms.ModelForm):
    to_box = forms.CharField(max_length=10, required=False, label='Boxes,Pieces')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        self.fields['to_qty'] = forms.CharField(required=False)
        self.fields['to_qty'].widget.attrs['value'] = instance.quantity
        self.fields['to_qty'].widget.attrs['readonly'] = True

        if hasattr(instance, 'product'):
            self.fields['to_box'].widget.attrs['value'] = self.instance.to_box
        else:
            print('no self.product')
    class Meta:
        model = SaleLineItem
        fields = '__all__'

    def clean_to_box(self):
        # value = self.instance.to_pieces
        data = self['to_box'].value()
        # lineitem = getattr(self, 'instance', None)
        # if not lineitem.id:
        prod = self['product'].value()
        self.instance.to_box_from_value(data, prod)
        # else:
        #     self.instance.to_box_from_value(data)
        return data

    # def clean(self):
    #     cleaned_data = super().clean()
    #     # q = self['quantity'].value()
    #     box_value = self['to_box'].value()
    #     # q1 = self.instance.quantity
    #     self.instance.to_box_from_value(box_value)
    #     # q2 = self.instance.quantity
    #     # print('Clearn called------ {} {}'.format(q1, q2))


ItemFormSet = forms.modelformset_factory(
    SaleLineItem,
    form=ItemForm,
)


class SaleForm(forms.ModelForm):

    class Meta:
        model = Sale
        exclude = []


ItemInlineFormSet = forms.inlineformset_factory(
    Sale,
    SaleLineItem,
    fields='__all__',
    form=ItemForm,
    formset=ItemFormSet,
    extra=1,
    min_num=1
)

DailySaleFormSet = forms.inlineformset_factory(Sale, SaleLineItem, fields=['product', 'linetotal', 'quantity_returned', 'posted'], form=ItemForm, extra=1)



# ============= Test Form ===============
class TestItemForm(forms.ModelForm):
    to_box = forms.CharField(max_length=100, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        print(self.instance.to_box)
        self.fields['to_box'].widget.attrs['value'] = self.instance.to_box

    class Meta:
        model = SaleLineItem
        fields = '__all__'

    def clean_to_box(self):
        # value = self.instance.to_pieces
        data = self['to_box'].value()
        self.instance.quantity = data
        return data

