from django.db import models
from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator

class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)  # Optional description
    country = models.CharField(max_length=100, blank=True)  # Example extra field: country of origin
    founded_year = models.PositiveIntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(1800), MaxValueValidator(now().year)]
    )  # Founded year must be realistic

    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE, related_name='car_models')
    dealer_id = models.IntegerField()
    name = models.CharField(max_length=100)
    
    CAR_TYPES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
    ]
    type = models.CharField(max_length=10, choices=CAR_TYPES, default='SUV')

    year = models.IntegerField(
        default=now().year,
        validators=[
            MinValueValidator(2015),
            MaxValueValidator(now().year)
        ]
    )

    color = models.CharField(max_length=50, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.car_make.name} {self.name}"

