from django.contrib import admin
from .models import Materials, Producers, MaterialType


admin.site.register(Materials)
admin.site.register(MaterialType)
admin.site.register(Producers)
