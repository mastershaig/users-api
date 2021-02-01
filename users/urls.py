from . import views
import debug_toolbar
from django.urls import include, path

urlpatterns = [
    path('__debug__/', include(debug_toolbar.urls)),
    path('', views.IndexView.as_view(), name='index'),
]
