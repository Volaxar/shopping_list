from django import forms

from shoplist.models import Purchase


class BaseDictForm(forms.ModelForm):
    error_css_class = 'error-field'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class PurchaseForm(BaseDictForm):

    class Meta:
        model = Purchase
        fields = ['id', 'name', 'amount', 'unit', 'category', 'priority']



