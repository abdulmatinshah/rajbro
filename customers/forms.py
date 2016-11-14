# from django import forms
# from sales.models import SaleLineItem





'''
ItemFormSet = forms.modelformset_factory(SaleLineItem)

class SaleForm(forms.ModelForm):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.item_formset = ItemFormSet(instance=self.instance,
                                        data=self.data or None,
                                        prefix=self.prefix)

    def is_valid(self):
        return super().is_valid() and self.item_formset.is_valid()

    def save(self, commit=True):
        # Supporting commit=False is another can of worms.  No use dealing
        # it before it's needed. (YAGNI)
        assert commit == True
        res = super().save(commit=commit)
        self.item_formset.save()
        return res
'''