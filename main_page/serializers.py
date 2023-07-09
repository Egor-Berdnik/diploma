from rest_framework import serializers
from .models import Materials, Producers, MaterialType


class ProducersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producers
        fields = "__all__"


class MaterialTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialType
        fields = "__all__"


class MaterialsSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    cost = serializers.FloatField()
    material_type = MaterialTypeSerializer(read_only=True)
    producer = ProducersSerializer(read_only=True)
    material_type_id = serializers.IntegerField()
    producer_id = serializers.IntegerField()

    def create(self, validated_data):
        return Materials.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.cost = validated_data.get('cost', instance.cost)
        instance.material_type_id = validated_data.get('material_type_id',
                                                       instance.material_type_id)
        instance.producer_id = validated_data.get('producer_id', instance.producer_id)
        instance.save()
        return instance
