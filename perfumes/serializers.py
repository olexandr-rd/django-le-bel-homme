from rest_framework import serializers
from le_bel_homme.models import Perfume

class PerfumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perfume
        fields = '__all__'