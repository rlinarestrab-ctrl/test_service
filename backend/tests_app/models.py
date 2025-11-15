import uuid
from django.db import models


class Test(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    duracion_minutos = models.IntegerField(null=True, blank=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    creador_id = models.UUIDField()  # Referencia lógica al auth_service

    def __str__(self):
        return self.titulo


class Pregunta(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    test = models.ForeignKey(Test, related_name="preguntas", on_delete=models.CASCADE)
    texto_pregunta = models.TextField()
    tipo = models.CharField(
        max_length=20,
        choices=[
            ("opcion_multiple", "Opción múltiple"),
            ("escala_likert", "Escala Likert"),
            ("abierta", "Abierta"),
        ],
    )
    orden = models.IntegerField()
    peso = models.DecimalField(max_digits=3, decimal_places=2, default=1.00)

    class Meta:
        ordering = ["orden"]

    def __str__(self):
        return f"{self.test.titulo} - {self.texto_pregunta[:40]}"


class OpcionRespuesta(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pregunta = models.ForeignKey(Pregunta, related_name="opciones", on_delete=models.CASCADE)
    texto_opcion = models.TextField()
    valor = models.CharField(max_length=50, blank=True, null=True)
    puntuacion = models.IntegerField(default=0)


class ResultadoTest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    test = models.ForeignKey(Test, related_name="resultados", on_delete=models.CASCADE)
    usuario_id = models.UUIDField()  # viene del auth_service
    fecha_completado = models.DateTimeField(auto_now_add=True)
    puntuacion_total = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    tiempo_transcurrido = models.IntegerField(null=True, blank=True)


class RespuestaUsuario(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    resultado_test = models.ForeignKey(ResultadoTest, related_name="respuestas", on_delete=models.CASCADE)
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    opcion_seleccionada = models.ForeignKey(OpcionRespuesta, on_delete=models.SET_NULL, null=True, blank=True)
    respuesta_texto = models.TextField(blank=True, null=True)


class CarreraSugerida(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    area_conocimiento = models.CharField(max_length=100)


class ResultadoCarrera(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    resultado_test = models.ForeignKey(ResultadoTest, related_name="carreras", on_delete=models.CASCADE)
    carrera = models.ForeignKey(CarreraSugerida, on_delete=models.CASCADE)
    compatibilidad = models.DecimalField(max_digits=5, decimal_places=2)
