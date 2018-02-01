from django.conf.urls import url, include
from django.views.generic.base import RedirectView

urlpatterns = [
    url(r'^$', RedirectView.as_view(pattern_name='purchase-list')),
    url(r'^shoplist/', include('shoplist.urls'))
]
