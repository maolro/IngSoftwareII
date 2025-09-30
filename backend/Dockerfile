FROM python:3.9-slim

WORKDIR /app/backend

# Copia e instala requisitos
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Expone el puerto
EXPOSE 8000

# Arranca la app
CMD ["python", "app.py"]