from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from binocularslive import views
from apis.views import HelloView, ByeView

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('hello/', HelloView.as_view(), name='hello'),
    path('bye/', ByeView.as_view(), name='bye'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
