#imagen base Python ligera
FROM python:3.9-slim

#directorio de trabajo 
WORKDIR /app

#copia el archivo  y lo instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#copia el resto de la aplicación
COPY . .

#expone el puerto en el que se ejecuta la aplicación
EXPOSE 5000

#comando para ejecutar la aplicación
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]