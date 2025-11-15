#!/bin/sh
set -e

# ============================================
#  VARS POR DEFECTO (solo si no vienen del entorno)
# ============================================
: "${POSTGRES_HOST:=db}"
: "${POSTGRES_PORT:=5432}"

# ============================================
#  ESPERAR A LA BASE DE DATOS (local y producción)
# ============================================
if [ -n "$POSTGRES_HOST" ]; then
  echo "🐘 Esperando a la base de datos en $POSTGRES_HOST:$POSTGRES_PORT..."
  while ! nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
    sleep 1
  done
  echo "✅ Base de datos lista."
else
  echo "⚠️ POSTGRES_HOST no definido, saltando espera de DB."
fi

# ============================================
#  MIGRACIONES
# ============================================
echo "🔄 Ejecutando migraciones..."
python manage.py migrate --noinput

# ============================================
#  ARCHIVOS ESTÁTICOS
# ============================================
echo "📦 Recopilando archivos estáticos..."
python manage.py collectstatic --noinput || true

# ============================================
#  SEED / DATOS INICIALES
# ============================================
echo "🌱 Insertando datos iniciales..."
python manage.py shell < tests_app/seed_data.py || true

# ============================================
#  INICIO DEL SERVIDOR
# ============================================
if [ "$DJANGO_DEBUG" = "False" ]; then
  echo "🚀 Iniciando Gunicorn (producción)..."
  exec gunicorn test_service.wsgi:application --bind 0.0.0.0:8000
else
  echo "🚀 Iniciando servidor Django (desarrollo)..."
  exec python -u manage.py runserver 0.0.0.0:8000
fi

