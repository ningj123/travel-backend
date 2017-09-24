from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.views.static import serve
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls
from rest_framework.authtoken import views

from users import views as users_views
from reserve import views as reserve_views
from api import APIUserView

router = DefaultRouter()
router.register(r'users', APIUserView)

urlpatterns = [
    url(r'^$', users_views.IndexView.as_view(), name='index'),
    url(r'^login/$', users_views.LoginView.as_view(), name='login'),
    url(r'^logout/$', users_views.LogoutView.as_view(), name='logout'),
    url(r'^signup', users_views.SignupView.as_view(), name='signup'),
    url(r'^admin/', admin.site.urls),
    url(r'^ucenter/$', users_views.UcenterView.as_view(), name='ucenter'),
    url(r'^media/(?P<path>.*)', serve, {"document_root": settings.MEDIA_ROOT}),
    url(r'^reserve/schoolbus/$', reserve_views.SchoolBusReserve.as_view(), name='schoolbusreserve'),
    url(r'^reserve/schoolbus/(?P<pk>[0-9]+)/$',reserve_views.SchoolBusReserveSuccess.as_view(), name='schoolbusreservesuccess'),
    url(r'^reserve/schoolbus/done/$', TemplateView.as_view(template_name='reserve/done.html'), name='schoolbusreservedone'),
    url(r'^reserve/seats/$', reserve_views.GetSeatsInfo.as_view(), name='seatsinfo'),

    url(r'^api/', include(router.urls, namespace='api')),
    url(r'^api/api-token-auth/', views.obtain_auth_token),
    url(r'^docs/', include_docs_urls(title='My API title'))
]