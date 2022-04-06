from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

app_name = "products"

urlpatterns = [
    path("products/", views.ProductList.as_view()),
    path("products/<int:pk>/", views.ProductDetail.as_view()),
    path("products/<int:pk>/funding/", views.ProductFunding.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
