from django import forms

from shoplist.models import Purchase, Unit, Category, Priority


class BaseDictForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            classes = ['form-control']

            if field in self.errors:
                classes.append('error-field')

            self.fields[field].widget.attrs['class'] = ' '.join(classes)


class UnitForm(BaseDictForm):
    class Meta:
        model = Unit
        fields = '__all__'


class CategoryForm(BaseDictForm):
    class Meta:
        model = Category
        fields = '__all__'


class PriorityForm(BaseDictForm):
    class Meta:
        model = Priority
        fields = '__all__'


class PurchaseForm(BaseDictForm):
    class Meta:
        model = Purchase
        fields = ['id', 'name', 'amount', 'unit', 'category', 'priority']
