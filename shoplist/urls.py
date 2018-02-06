from django.conf.urls import url

from shoplist.models import Unit, Category, Priority
from . import views

urlpatterns = [
    url(r'^$', views.PurchaseList.as_view(), name='purchase-list'),
    url(r'^create/', views.PurchaseCreate.as_view(), name='purchase-create'),
    url(r'^(?P<pk>[0-9]+)/$', views.PurchaseUpdate.as_view(), name='purchase-update'),
    url(r'^(?P<pk>[0-9]+)/delete/$', views.PurchaseDelete.as_view(), name='purchase-delete'),

    url(r'^(?P<pk>[0-9]+)/change_status/$', views.change_status, name='change-status'),

    url(r'^unit/list/$', views.UnitList.as_view(), name='unit-list'),
    url(r'^category/list/$', views.CategoryList.as_view(), name='category-list'),
    url(r'^priority/list$', views.PriorityList.as_view(), name='priority-list'),

    url(r'^unit/(?P<pk>[0-9]*)', views.UnitView.as_view()),
    url(r'^category/(?P<pk>[0-9]*)', views.CategoryView.as_view()),
    url(r'^priority/(?P<pk>[0-9]*)', views.PriorityView.as_view()),
]
