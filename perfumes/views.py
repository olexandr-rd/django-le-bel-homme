from rest_framework import viewsets, permissions

from le_bel_homme.models import Perfume
from perfumes.serializers import PerfumeSerializer


# Create your views here.
class PerfumeViewSet(viewsets.ModelViewSet):
    queryset = Perfume.objects.all()
    serializer_class = PerfumeSerializer
    permission_classes = [permissions.IsAuthenticated]