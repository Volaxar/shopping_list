from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^unit/list/$', views.UnitList.as_view(), name='unit-list'),
    url(r'^category/list/$', views.CategoryList.as_view(), name='category-list'),
    url(r'^priority/list/$', views.PriorityList.as_view(), name='priority-list'),
    url(r'^purchase/list/$', views.PurchaseList.as_view(), name='purchase-list'),

    url(r'^unit/(?P<pk>[0-9]*)', views.UnitView.as_view()),
    url(r'^category/(?P<pk>[0-9]*)', views.CategoryView.as_view()),
    url(r'^priority/(?P<pk>[0-9]*)', views.PriorityView.as_view()),
    url(r'^purchase/(?P<pk>[0-9]*)', views.PurchaseView.as_view()),
]
