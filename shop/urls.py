from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add/<int:item_id>/', views.add_to_order, name='add_to_order'),
    path('buy/<int:item_id>/', views.buy_now, name='buy_now'),
    path('order/', views.order_view, name='order'),
    path('pay-order/', views.pay_order, name='pay_order'),
    path('success/', views.success, name='success'),
    path('cancel/', views.cancel, name='cancel'),
    path('order/item/<int:order_item_id>/cancel/', views.cancel_order_item, name='cancel_order_item'),
]
