import csv
import os
from django.core.management.base import BaseCommand
from products.models import Product
from django.conf import settings


class Command(BaseCommand):
    help = "Import first 10,000 products from train.csv"

    def handle(self, *args, **kwargs):
        csv_path = os.path.join(settings.BASE_DIR, "data", "train.csv")

        if not os.path.exists(csv_path):
            self.stdout.write(self.style.ERROR("CSV file not found"))
            return

        count = 0
        limit = 10000

        with open(csv_path, encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                if count >= limit:
                    break

                Product.objects.update_or_create(
                    product_id=int(row["PRODUCT_ID"]),
                    defaults={
                        "title": row.get("TITLE", "")[:255],
                        "description": row.get("DESCRIPTION", ""),
                        "bullet_points": row.get("BULLET_POINTS", ""),
                        "product_type_id": row.get("PRODUCT_TYPE_ID") or None,
                        "product_length": row.get("PRODUCT_LENGTH") or None,
                    }
                )

                count += 1

        self.stdout.write(
            self.style.SUCCESS(f"{count} products imported successfully")
        )
