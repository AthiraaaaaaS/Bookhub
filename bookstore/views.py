from rest_framework import viewsets
from .models import Book, Order
from .serializers import BookSerializer, OrderSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
import pandas as pd
import numpy as np

from django.http import HttpResponse

def home(request):
    return HttpResponse("<h1>Welcome to Bookhub</h1>")

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

@api_view(['GET'])
def order_summary(request):
    orders = Order.objects.all().values()
    df = pd.DataFrame(orders)

    if df.empty:
        return Response({'message': 'No orders yet'})

    #Lambda usage examples
    book_titles = list(map(lambda order: order['book_id'], orders))
    completed_orders = list(filter(lambda o: o['status'] == 'Completed', orders))
    sorted_by_quantity = sorted(orders, key=lambda o: o['quantity'], reverse=True)

    #Convert Decimal to float before rounding
    total_revenue = float(df['total_price'].sum())
    avg_order_value = float(df['total_price'].mean())
    total_quantity = int(df['quantity'].sum())

    stats = {
        'total_revenue': round(total_revenue, 2),
        'average_order_value': round(avg_order_value, 2),
        'total_books_sold': total_quantity,
        'book_ids': book_titles,
        'completed_order_count': len(completed_orders),
        'top_order_by_quantity': sorted_by_quantity[0] if sorted_by_quantity else None,
    }
    return Response(stats)

@api_view(['GET'])
def export_orders_csv(request):
    orders = Order.objects.all().values()
    df = pd.DataFrame(orders)

    if df.empty:
        return Response({'message': 'No orders to export'})

    csv_data = df.to_csv(index=False)
    return Response({'csv': csv_data})
