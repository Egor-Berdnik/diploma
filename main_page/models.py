from django.db import models


class Materials(models.Model):
    name = models.CharField(max_length=100)
    producer = models.CharField(max_length=100)
    cost = models.IntegerField()
    material_type = models.CharField(max_length=100)

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
