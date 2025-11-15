from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from collections import defaultdict

from .models import Test, Pregunta, ResultadoTest, RespuestaUsuario, CarreraSugerida
from .serializers import (
    TestSerializer,
    ResultadoTestSerializer,
    CarreraSugeridaSerializer,
)

# 🧩 1️⃣ ViewSet para los tests
class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    permission_classes = [permissions.AllowAny]


# 🧩 2️⃣ ViewSet para las carreras sugeridas
class CarreraSugeridaViewSet(viewsets.ModelViewSet):
    queryset = CarreraSugerida.objects.all()
    serializer_class = CarreraSugeridaSerializer
    permission_classes = [permissions.AllowAny]


# 🧩 3️⃣ ViewSet para los resultados
class ResultadoTestViewSet(viewsets.ModelViewSet):
    queryset = ResultadoTest.objects.all()
    serializer_class = ResultadoTestSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=["get"], url_path="mis-resultados/(?P<usuario_id>[0-9a-f-]+)")
    def mis_resultados(self, request, usuario_id=None):
        resultados = self.queryset.filter(usuario_id=usuario_id)
        serializer = self.get_serializer(resultados, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="evaluar")
    @transaction.atomic
    def evaluar(self, request):
        """
        Recibe respuestas del usuario, calcula el perfil RIASEC
        y devuelve carreras sugeridas basadas en las áreas más altas.
        """
        data = request.data
        usuario_id = data.get("usuario_id")
        test_id = data.get("test_id")
        respuestas = data.get("respuestas")

        if not usuario_id or not test_id or not respuestas:
            return Response(
                {"error": "Faltan datos: usuario_id, test_id o respuestas."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            test = Test.objects.get(id=test_id)
        except Test.DoesNotExist:
            return Response(
                {"error": f"El test con ID {test_id} no existe."},
                status=status.HTTP_404_NOT_FOUND,
            )

        area_puntajes = defaultdict(list)
        for r in respuestas:
            try:
                pregunta = Pregunta.objects.get(id=r["pregunta_id"])
                puntuacion = int(r["puntuacion"])
                if "[" in pregunta.texto_pregunta and "]" in pregunta.texto_pregunta:
                    area = pregunta.texto_pregunta.split("]")[0].replace("[", "").strip()
                    area_puntajes[area].append(puntuacion)
            except (Pregunta.DoesNotExist, KeyError, ValueError):
                continue

        if not area_puntajes:
            return Response(
                {"error": "No se pudieron determinar áreas RIASEC a partir de las respuestas."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        resultados_area = {
            area: (sum(v) / len(v) if v else 0) for area, v in area_puntajes.items()
        }
        top_areas = sorted(resultados_area.items(), key=lambda x: x[1], reverse=True)[:3]
        codigo_holland = "".join([a[0][0].upper() for a in top_areas])

        resultado = ResultadoTest.objects.create(
            test=test,
            usuario_id=usuario_id,
            puntuacion_total=sum(resultados_area.values()),
            tiempo_transcurrido=data.get("tiempo_transcurrido", 0),
        )

        for r in respuestas:
            try:
                pregunta = Pregunta.objects.get(id=r["pregunta_id"])
                puntuacion = int(r["puntuacion"])
                RespuestaUsuario.objects.create(
                    resultado_test=resultado,
                    pregunta=pregunta,
                    respuesta_texto=str(puntuacion),
                )
            except Exception:
                continue

        carreras = CarreraSugerida.objects.filter(
            area_conocimiento__in=[a[0] for a in top_areas]
        )
        carreras_data = CarreraSugeridaSerializer(carreras, many=True).data

        response_data = {
            "usuario_id": usuario_id,
            "test": test.titulo,
            "codigo_holland": codigo_holland,
            "resultados_area": resultados_area,
            "top_areas": [a[0] for a in top_areas],
            "carreras_recomendadas": carreras_data,
        }

        return Response(response_data, status=status.HTTP_200_OK)
