from django.db import models

# Create your models here.
from django.db import models

class Product(models.Model):
    product_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    bullet_points = models.TextField(blank=True)
    product_type_id = models.IntegerField(null=True, blank=True)
    product_length = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.title

