from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import PerfumeViewSet

router = DefaultRouter()
router.register('perfumes', PerfumeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
