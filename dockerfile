# 1. La Imagen Base
FROM python:3.11-slim

# 2. El Directorio de Trabajo que se creará en el contenedor
WORKDIR /app

# 3. Copiar las recetas de las librerías
COPY requirements.txt .

# 4. Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiar el resto del código
COPY . .

# 6. El comando de ejecución (para FastAPI) ¡ojo! src.main (ya que main.py no se encuentra en la cpta raiz)
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]