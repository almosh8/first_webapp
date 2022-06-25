from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('imports', views.add_items, name='import'),
    path('delete/<str:pk>', views.delete, name='delete'),
    path('nodes/<str:pk>', views.nodes, name='nodes'),
    path('sales', views.sales, name='sales'),
    path('node/<str:pk>/statistic', views.statistic, name='statistic'),
]