# ---------------------------------------------------------------------------
# Frontend RoboMaze (HTML + CSS + JavaScript estáticos)
# ---------------------------------------------------------------------------
# Es un sitio estático: no necesita Node ni build. Lo sirve Nginx directamente.
FROM nginx:1.27-alpine

# Configuración propia de Nginx (sustituye la del sitio por defecto).
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copiar los archivos del sitio a la raíz pública de Nginx.
COPY . /usr/share/nginx/html

# Nginx escucha en el puerto 80 dentro del contenedor.
EXPOSE 80
