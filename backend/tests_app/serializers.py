from rest_framework import serializers
from .models import *


class OpcionRespuestaSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpcionRespuesta
        fields = "__all__"


class PreguntaSerializer(serializers.ModelSerializer):
    opciones = OpcionRespuestaSerializer(many=True, read_only=True)

    class Meta:
        model = Pregunta
        fields = "__all__"


class TestSerializer(serializers.ModelSerializer):
    preguntas = PreguntaSerializer(many=True, read_only=True)

    class Meta:
        model = Test
        fields = "__all__"


class RespuestaUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = RespuestaUsuario
        fields = "__all__"


class ResultadoTestSerializer(serializers.ModelSerializer):
    respuestas = RespuestaUsuarioSerializer(many=True, read_only=True)

    class Meta:
        model = ResultadoTest
        fields = "__all__"


class CarreraSugeridaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarreraSugerida
        fields = "__all__"


class ResultadoCarreraSerializer(serializers.ModelSerializer):
    carrera = CarreraSugeridaSerializer(read_only=True)

    class Meta:
        model = ResultadoCarrera
        fields = "__all__"
