from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.generic import ListView
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.edit import ModelFormMixin, ProcessFormView, DeletionMixin
from django.http.response import Http404

from shoplist.forms import PurchaseForm, UnitForm, CategoryForm, PriorityForm
from shoplist.models import Purchase, Unit, Category, Priority


class DictList(ListView):
    fields = []

    template_name = 'shoplist/dict_list.html'
    template_ajax_name = 'shoplist/_dict_list.html'

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            self.template_name = self.template_ajax_name

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['fields'] = self.fields
        context['model_name'] = self.model.get_name()
        context['model_verbose_name'] = self.model.get_verbose_name_plural()

        return context

    def delete(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)


class PurchaseList(DictList):
    model = Purchase
    fields = ['name', 'amount', 'unit', 'category', 'priority']

    template_name = 'shoplist/purchase_list.html'
    template_ajax_name = 'shoplist/_purchase_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['name_filter'] = self.request.session.get('filter', '')
        context['order_by'] = self.request.session.get('order_by', '')
        context['order_direction'] = self.request.session.get('order_direction', '')

        return context

    def get_queryset(self):
        r = self.request

        if 'filter' in r.GET:
            name_filter = r.GET['filter']
            r.session['filter'] = name_filter
        else:
            name_filter = r.session.get('filter', '')

        order_by = r.session.get('order_by', 'name')
        order_by_direction = r.session.get('order_direction', '')

        if 'order_by' in r.GET:
            if r.GET['order_by'] != order_by:
                order_by = r.GET['order_by']
                order_by_direction = ''
            else:
                order_by_direction = '' if order_by_direction else '-'

            r.session['order_by'] = order_by
            r.session['order_direction'] = order_by_direction

        return Purchase.objects.filter(name__icontains=name_filter).order_by('%s%s' % (order_by_direction, order_by))


class UnitList(DictList):
    model = Unit
    fields = ['name']


class CategoryList(DictList):
    model = Category
    fields = ['name']


class PriorityList(DictList):
    model = Priority
    fields = ['name']


class BaseDictView(ModelFormMixin, ProcessFormView, DeletionMixin):
    pass


class DictView(SingleObjectTemplateResponseMixin, BaseDictView):
    object = None
    template_name = 'shoplist/dict_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.object = None

        try:
            if kwargs.get('pk', ''):
                self.object = self.get_object()
        except Http404:
            pass

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if not request.is_ajax():
            return redirect('purchase-list')

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return JsonResponse({
                'response': self.form_invalid(form).rendered_content
            })

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class UnitView(DictView):
    model = Unit
    form_class = UnitForm


class CategoryView(DictView):
    model = Category
    form_class = CategoryForm


class PriorityView(DictView):
    model = Priority
    form_class = PriorityForm


class PurchaseView(DictView):
    model = Purchase
    form_class = PurchaseForm

    @staticmethod
    def patch(request, *args, **kwargs):
        pk = kwargs.get('pk', '')

        if pk:
            Purchase.change_status(pk)

        return redirect('purchase-list')
