import csv
import os
from django.core.management.base import BaseCommand
from products.models import Product

class Command(BaseCommand):
    help = "Load products from CSV"

    def handle(self, *args, **kwargs):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        csv_path = os.path.join(base_dir, 'data', 'train.csv')

        count = 0
        with open(csv_path, encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Product.objects.update_or_create(
                    product_id=int(row['PRODUCT_ID']),
                    defaults={
                        'title': row['TITLE'][:255],
                        'description': row.get('DESCRIPTION', ''),
                        'bullet_points': row.get('BULLET_POINTS', ''),
                        'product_type_id': row.get('PRODUCT_TYPE_ID') or None,
                        'product_length': row.get('PRODUCT_LENGTH') or None,
                    }
                )
                count += 1

        self.stdout.write(self.style.SUCCESS(f"{count} products loaded successfully"))
