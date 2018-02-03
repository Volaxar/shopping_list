from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.PurchaseList.as_view(), name='purchase-list'),
    url(r'^create/', views.PurchaseCreate.as_view(), name='purchase-create'),
    url(r'^(?P<pk>[0-9]+)/$', views.PurchaseUpdate.as_view(), name='purchase-update'),
    url(r'^(?P<pk>[0-9]+)/delete/$', views.PurchaseDelete.as_view(), name='purchase-delete'),

    url(r'^(?P<pk>[0-9]+)/change_status/$', views.change_status, name='change-status'),
]
