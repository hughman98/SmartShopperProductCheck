from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('details/', views.ProductDetailsAPIView.as_view(), name='product-details'),
    path('', views.home, name='home'),
    path('result_page', views.result_page, name='result_page')
]


