from django import forms

from shoplist.models import Purchase


class PurchaseForm(forms.ModelForm):
    id = forms.IntegerField(widget=forms.HiddenInput)

    class Meta:
        model = Purchase
        fields = ['id', 'name', 'amount', 'unit', 'category', 'priority', 'status']
