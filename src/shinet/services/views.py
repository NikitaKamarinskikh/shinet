from rest_framework.generics import ListAPIView
from .models import Specializations
from .serializers import SpecializationsListSerializer


class SpecializationsAPIView(ListAPIView):
    serializer_class = SpecializationsListSerializer
    queryset = Specializations.objects.all()

