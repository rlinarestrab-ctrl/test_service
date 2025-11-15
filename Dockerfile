# Usa imagen base de Python
FROM python:3.11-slim

# Evitar buffers y errores de encoding
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y libpq-dev gcc netcat-traditional && rm -rf /var/lib/apt/lists/*

# Configurar el directorio de trabajo
WORKDIR /app

# Copiar dependencias
COPY backend/requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY backend /app

# Copiar entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Exponer puerto de Django
EXPOSE 8000

# Comando de entrada
ENTRYPOINT ["/entrypoint.sh"]
