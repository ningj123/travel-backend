from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.views.static import serve

from users import views as users_views

urlpatterns = [
    url(r'^$', users_views.IndexView.as_view(), name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'^ucenter/$', users_views.UcenterView.as_view(), name='ucenter'),
    url(r'^media/(?P<path>.*)', serve, {"document_root": settings.MEDIA_ROOT}),
]
