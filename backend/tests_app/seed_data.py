from django.db import transaction
from tests_app.models import Test, Pregunta, OpcionRespuesta, CarreraSugerida

@transaction.atomic
def seed_riasec():
    # 🔍 1) Ver si el test ya existe
    test, created = Test.objects.get_or_create(
        titulo="Test RIASEC de Holland",
        defaults={
            "descripcion": (
                "Evalúa tus intereses vocacionales en seis áreas: "
                "Realista (R), Investigador (I), Artístico (A), Social (S), "
                "Emprendedor (E) y Convencional (C). "
                "El test ayuda a identificar tus inclinaciones profesionales "
                "para orientar tu elección de carrera."
            ),
            "duracion_minutos": 20,
            "creador_id": "00000000-0000-0000-0000-000000000000",
        },
    )

    if not created:
        print("⚠️ Test RIASEC ya existía. No se creó uno nuevo.")
        return  # Importante: salimos para no duplicar preguntas/opciones

    preguntas_por_area = {
        "Realista": [
            "Disfruto trabajar con mis manos o herramientas.",
            "Me gusta reparar o armar cosas mecánicas o electrónicas.",
            "Prefiero actividades al aire libre en lugar de una oficina.",
            "Me interesa la maquinaria, vehículos o construcción.",
        ],
        "Investigador": [
            "Me gusta resolver problemas complejos o lógicos.",
            "Disfruto realizar experimentos o investigaciones.",
            "Prefiero entender cómo funcionan las cosas antes de usarlas.",
            "Me interesa la ciencia, las matemáticas o la tecnología.",
        ],
        "Artístico": [
            "Me gusta expresarme a través del arte, música o escritura.",
            "Disfruto crear cosas originales o diferentes.",
            "Prefiero trabajos sin rutinas rígidas o repetitivas.",
            "Me atraen las actividades creativas o visuales.",
        ],
        "Social": [
            "Me gusta ayudar a los demás a resolver sus problemas.",
            "Disfruto enseñar, orientar o escuchar a otras personas.",
            "Prefiero trabajar en grupo antes que solo.",
            "Me interesan las profesiones relacionadas con la educación o la salud.",
        ],
        "Emprendedor": [
            "Me gusta liderar proyectos o equipos.",
            "Disfruto convencer o motivar a otros.",
            "Prefiero tomar decisiones y asumir riesgos.",
            "Me interesan los negocios, las ventas o la política.",
        ],
        "Convencional": [
            "Me gusta mantener el orden y seguir procedimientos claros.",
            "Disfruto trabajar con datos, números o registros.",
            "Prefiero tareas organizadas y bien estructuradas.",
            "Me interesa la contabilidad, la administración o la oficina.",
        ],
    }

    orden = 1
    for area, preguntas in preguntas_por_area.items():
        for texto in preguntas:
            p = Pregunta.objects.create(
                test=test,
                texto_pregunta=f"[{area}] {texto}",
                tipo="escala_likert",
                orden=orden,
                peso=1.0,
            )
            opciones = [
                ("Nada de acuerdo", 1),
                ("Poco de acuerdo", 2),
                ("Algo de acuerdo", 3),
                ("Bastante de acuerdo", 4),
                ("Totalmente de acuerdo", 5),
            ]
            for txt, val in opciones:
                OpcionRespuesta.objects.create(
                    pregunta=p,
                    texto_opcion=txt,
                    puntuacion=val,
                )
            orden += 1

    print("✅ Test RIASEC completo creado con 24 preguntas.")


@transaction.atomic
def seed_carreras():
    carreras_por_area = {
        "Realista": [
            ("Ingeniería Mecánica", "Diseño, operación y mantenimiento de máquinas e instalaciones."),
            ("Arquitectura", "Diseño y construcción de edificaciones funcionales y estéticas."),
            ("Electricidad Industrial", "Instalación y mantenimiento de sistemas eléctricos."),
        ],
        "Investigador": [
            ("Biología", "Estudio de los seres vivos y sus interacciones con el entorno."),
            ("Ciencias de la Computación", "Desarrollo de software, algoritmos y sistemas inteligentes."),
            ("Medicina", "Diagnóstico y tratamiento de enfermedades humanas."),
        ],
        "Artístico": [
            ("Diseño Gráfico", "Creación visual y comunicación a través de elementos gráficos."),
            ("Música", "Composición, interpretación y producción musical."),
            ("Artes Plásticas", "Expresión creativa mediante pintura, escultura y dibujo."),
        ],
        "Social": [
            ("Psicología", "Estudio del comportamiento humano y sus procesos mentales."),
            ("Educación", "Formación de personas a través de la enseñanza y orientación."),
            ("Trabajo Social", "Apoyo a comunidades y personas para mejorar su bienestar."),
        ],
        "Emprendedor": [
            ("Administración de Empresas", "Gestión de recursos, liderazgo y toma de decisiones."),
            ("Marketing", "Diseño de estrategias para posicionar productos y servicios."),
            ("Derecho", "Interpretación y aplicación de leyes en diversos contextos."),
        ],
        "Convencional": [
            ("Contaduría Pública", "Gestión y control de la información financiera."),
            ("Secretariado Ejecutivo", "Organización administrativa y comunicación empresarial."),
            ("Finanzas", "Análisis y gestión de inversiones y presupuestos."),
        ],
    }

    for area, carreras in carreras_por_area.items():
        for nombre, descripcion in carreras:
            obj, created = CarreraSugerida.objects.get_or_create(
                nombre=nombre,
                defaults={
                    "descripcion": descripcion,
                    "area_conocimiento": area,
                },
            )
            if created:
                print(f"✅ Carrera creada: {nombre} ({area})")
            else:
                print(f"ℹ️ Carrera ya existía: {nombre} ({area})")

    print("✅ Carreras sugeridas creadas/validada por área RIASEC.")


def seed_all():
    seed_riasec()
    seed_carreras()
    print("\n🎯 Base de datos inicial del servicio de test completada exitosamente.")


# ❌ IMPORTANTE: ya NO se llama seed_all() automáticamente aquí.
# Lo vas a invocar tú desde el entrypoint o manualmente.
