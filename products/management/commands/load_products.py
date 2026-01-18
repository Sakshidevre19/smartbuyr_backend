import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from products.models import Product

class Command(BaseCommand):
    help = "Load first 10,000 products from CSV"

    def handle(self, *args, **kwargs):

        # BASE_DIR = SmartBuyr/backend
        csv_path = os.path.join(settings.BASE_DIR, "data", "train.csv")

        if not os.path.exists(csv_path):
            self.stderr.write(self.style.ERROR(f"CSV file not found: {csv_path}"))
            return

        max_rows = 10000
        count = 0

        with open(csv_path, encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                if count >= max_rows:
                    break

                Product.objects.update_or_create(
                    product_id=int(row["PRODUCT_ID"]),
                    defaults={
                        "title": row["TITLE"][:255],
                        "description": row.get("DESCRIPTION", ""),
                        "bullet_points": row.get("BULLET_POINTS", ""),
                        "product_type_id": row.get("PRODUCT_TYPE_ID") or None,
                        "product_length": row.get("PRODUCT_LENGTH") or None,
                    },
                )
                count += 1

        self.stdout.write(
            self.style.SUCCESS(f"{count} products loaded successfully (limit = 10,000)")
        )
