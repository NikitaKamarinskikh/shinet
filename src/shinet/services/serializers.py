from rest_framework import serializers
from .models import Specializations


class SpecializationsListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Specializations
        fields = '__all__'


