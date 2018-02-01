from django.conf.urls import url

from .views import PurchaseList, PurchaseCreate, PurchaseUpdate, PurchaseDelete

urlpatterns = [
    url(r'^$', PurchaseList.as_view(), name='purchase-list'),
    url(r'^create/', PurchaseCreate.as_view(), name='purchase-create'),
    url(r'^(?P<pk>[0-9]+)/$', PurchaseUpdate.as_view(), name='purchase-update'),
    url(r'^(?P<pk>[0-9]+)/delete/$', PurchaseDelete.as_view(), name='purchase-delete'),
]
