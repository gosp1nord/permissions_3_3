from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet
from .models import Advertisement
from .serializers import AdvertisementSerializer
from .permissions import IsOwnerOrReadOnly
from .filters import AdvertisementFilter
from django.db.models import Q



class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly]
    filterset_class = AdvertisementFilter
    filter_backends = [DjangoFilterBackend]


    def get_queryset(self):
        user = self.request.user.id
        if self.request.user.is_staff:
            queryset = Advertisement.objects.all()
        else:
            queryset = Advertisement.objects.all().exclude(~Q(creator_id=user), status='DRAFT')
        return queryset

