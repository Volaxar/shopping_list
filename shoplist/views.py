from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from shoplist.forms import PurchaseForm
from shoplist.models import Purchase


class PurchaseList(ListView):
    model = Purchase

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            self.template_name = 'shoplist/_purchase_list.html'

        return super().get(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)

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


class PurchaseCreate(CreateView):
    model = Purchase
    fields = ['name', 'amount', 'unit', 'category', 'priority', 'purchased']


class PurchaseUpdate(UpdateView):
    model = Purchase
    form_class = PurchaseForm


class PurchaseDelete(DeleteView):
    model = Purchase
    success_url = reverse_lazy('purchase-list')
