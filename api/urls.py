from django.urls import path
from . import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls import url

app_name = "api"

schema_view = get_schema_view(
   openapi.Info(
      title="Code Task API",
      default_version='v1',
      description="This is the description for coding task",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="khaligli@hotmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Swagger Urls
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # User
    path('users', views.UsersApiView.as_view(), name="users"),
    path('average-age', views.AverageAgeView.as_view(), name="average_age"),
    path('letter-digit', views.LetterDigitView.as_view(), name="letter_digit"),


    # path('fakedata', views.FakeDataView.as_view(), name="fake-data"),

]
