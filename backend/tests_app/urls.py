from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TestViewSet, ResultadoTestViewSet, CarreraSugeridaViewSet

router = DefaultRouter()
router.register(r"tests", TestViewSet, basename="tests")
router.register(r"resultados", ResultadoTestViewSet, basename="resultados")
router.register(r"carreras", CarreraSugeridaViewSet, basename="carreras")

urlpatterns = router.urls
