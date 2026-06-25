# ---------------------------------------------------------------------------
# Backend RoboMaze API (FastAPI + Uvicorn)
# ---------------------------------------------------------------------------
# Imagen base ligera con Python. "slim" reduce el tamaño frente a la completa.
FROM python:3.12-slim

# Buenas prácticas de Python en contenedores:
#  - PYTHONDONTWRITEBYTECODE: no genera archivos .pyc
#  - PYTHONUNBUFFERED: los logs salen de inmediato (sin buffer)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# 1) Instalar dependencias primero (capa cacheable: solo se reconstruye
#    cuando cambia requirements.txt, no con cada cambio de código).
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2) Copiar el código de la aplicación.
COPY app ./app

# Puerto interno del contenedor donde escucha Uvicorn.
EXPOSE 8001

# Comprobación de salud usando el endpoint /api/v1/health (sin depender de curl).
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request,sys; sys.exit(0) if urllib.request.urlopen('http://127.0.0.1:8001/api/v1/health').status==200 else sys.exit(1)"

# Arranque del servidor. host 0.0.0.0 para aceptar conexiones desde fuera del contenedor.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
