# ---------- Backend (Python Flask) ----------

# Obtiene imagen de python
    FROM python:3.11-slim AS backend 

# Entra a directorio de trabajo e instala todas las librerías
WORKDIR /backend 
COPY backend/requirements.txt .
RUN pip install -r requirements.txt

# Mete la carpeta backend a la imagen
COPY backend .

# ---------- Frontend (React Native con Expo) ----------

# Obtiene la imagen de node
FROM node:20 AS frontend

# Instala todos los paquetes necesarios
WORKDIR /frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm install

# Mete la carpeta backend a la imagen
COPY frontend .

# ---------- Imagen combinada final ----------
FROM python:3.11-slim

# Copia el backend
WORKDIR /app/backend
COPY --from=backend /backend .

# Copia el frontend
WORKDIR /app/frontend
COPY --from=frontend /frontend .

# Instala Node para Expo en la imagen final
RUN apt-get update && apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g expo-cli

# Expone backend (Flask) y frontend (Expo)
EXPOSE 5000 19000 19001 19002

# Arranca ambos servicios
CMD ["sh", "-c", "python /app/backend/app.py & cd /app/frontend && npx expo start --tunnel"]