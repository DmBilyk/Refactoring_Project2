from django.urls import path
from . import views




urlpatterns = [
    path('', views.index, name='index'),
    path('case/', views.case_selection, name='case_selection'),
    path('processor/', views.processor_selection, name='processor_selection'),
    path('memory/', views.memory_selection, name='memory_selection'),
    path('storage/', views.storage_selection, name='storage_selection'),
    path('graphics/', views.graphics_selection, name='graphics_selection'),
    path('color/', views.color_selection, name='color_selection'),
    path('peripherals/', views.peripherals_selection, name='peripherals_selection'),
    path('device-type/', views.device_type_selection, name='device_type_selection'),
    path('summary/', views.summary, name='summary'),
    path('success/<int:order_id>/', views.order_success, name='order_success'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
]