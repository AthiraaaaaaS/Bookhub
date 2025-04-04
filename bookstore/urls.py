from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, OrderViewSet, order_summary, export_orders_csv
from . import views

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/order-summary/', order_summary),
    path('api/export-orders/', export_orders_csv),
    path('', views.home, name='home'),
]

