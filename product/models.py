from django.db import models

class Product(models.Model):
    # Fields for your product
    productId = models.CharField(max_length=100, unique=True)
    productName = models.CharField(max_length=255)
    productPrice = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.productName

    class Meta:
        # Optional: Add any meta options like ordering
        ordering = ['productId']
