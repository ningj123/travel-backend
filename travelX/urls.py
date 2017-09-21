from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.views.static import serve

from users import views as users_views
from reserve import views as reserve_views

urlpatterns = [
    url(r'^$', users_views.IndexView.as_view(), name='index'),
    url(r'^login/$', users_views.LoginView.as_view(), name='login'),
    url(r'^logout/$', users_views.LogoutView.as_view(), name='logout'),
    url(r'^signup', users_views.SignupView.as_view(), name='signup'),
    url(r'^admin/', admin.site.urls),
    url(r'^ucenter/$', users_views.UcenterView.as_view(), name='ucenter'),
    url(r'^media/(?P<path>.*)', serve, {"document_root": settings.MEDIA_ROOT}),
    url(r'^reserve/schoolbus/$', reserve_views.SchoolBusReserve.as_view(), name='schoolbusreserve'),
    url(r'^reserve/seats/$', reserve_views.GetSeatsInfo.as_view(), name='seatsinfo')
]
