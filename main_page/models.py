from django.db import models
from django.db.models import ForeignKey
from django.urls import reverse


class Materials(models.Model):
    name = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=5, decimal_places=2)
    material_type = models.ForeignKey('MaterialType', on_delete=models.PROTECT, null=True)
    producer = models.ForeignKey('Producers', on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Material"
        verbose_name_plural = "Materials"

    def get_absolute_url(self):
        return reverse('material_detail', kwargs={'pk': self.pk})


class Producers(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=13)
    foundation_year = models.CharField(max_length=4)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Producer"
        verbose_name_plural = "Producers"

    def get_absolute_url(self):
        return reverse('producer_detail', kwargs={'pk': self.pk})


class MaterialType(models.Model):
    name = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return self.name
