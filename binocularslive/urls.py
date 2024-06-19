from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from binocularslive import views
from apis.views import PermissionTestView, SplitView

title = "Binoculars Live"
admin.site.site_header = title
admin.site.site_title = title

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('permission_test/', PermissionTestView.as_view(),
         name='permission_test'),
    path('split/', SplitView.as_view(), name='split'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
