import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'solyn.settings')
django.setup()

from django.db import connection

def inspect_sequences():
    with connection.cursor() as cursor:
        print("Existing sequences in sqlite_sequence:")
        try:
            cursor.execute("SELECT * FROM sqlite_sequence")
            for row in cursor.fetchall():
                print(row)
        except Exception as e:
            print(f"Error reading sequence: {e}")

if __name__ == "__main__":
    inspect_sequences()
