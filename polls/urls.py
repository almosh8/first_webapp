from django.urls import path

from . import views

urlpatterns = [
    path('imports', views.add_items, name='import'),
    path('delete/<str:pk>', views.delete, name='delete'),
    path('nodes/<str:pk>', views.export_items, name='export'),
    path('sales', views.sales, name='sales'),
    path('node/<str:pk>/statistic', views.statistic, name='statistic'),
]