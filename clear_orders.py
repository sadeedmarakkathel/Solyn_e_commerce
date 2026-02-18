import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'solyn.settings')
django.setup()

from apps.orders.models import Order, OrderItem
from django.db import connection

def clear_all_orders():
    print("Deleting all OrderItems...")
    OrderItem.objects.all().delete()
    print("Deleting all Orders...")
    Order.objects.all().delete()
    
    # Reset ID sequence
    print("Resetting ID sequence...")
    table_name = Order._meta.db_table
    seq_name = f"{table_name}_id_seq"
    print(f"Target sequence: {seq_name}")
    with connection.cursor() as cursor:
        try:
            # For PostgreSQL
            cursor.execute(f"ALTER SEQUENCE {seq_name} RESTART WITH 1")
        except Exception as e:
            print(f"Sequence reset failed (non-critical): {e}")
    
    print("Successfully cleared all orders. Next order will be #1.")

if __name__ == "__main__":
    clear_all_orders()
