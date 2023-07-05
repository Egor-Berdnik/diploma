from django.db import models
from django.db.models import ForeignKey
from django.urls import reverse


class Producers(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=13)
    foundation_date = models.CharField(max_length=4)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Producer"
        verbose_name_plural = "Producers"


class Materials(models.Model):
    name = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=5, decimal_places=2)
    material_type = models.CharField(max_length=100)
    producer = models.ForeignKey(Producers, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Material"
        verbose_name_plural = "Materials"


class Calculations(models.Model):
    wall_area = models.IntegerField()
    width_wall = models.IntegerField()
    height_wall = models.IntegerField()

    def __str__(self):
        return self.wall_area
