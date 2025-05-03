#rodar docker
#docker-compose up --build
#docker-compose exec web python -m unittest discover -s testes


#parar e apagar os containers
#docker-compose down -v

# Dockerfile

FROM python:3.11-slim

# Define o diretório de trabalho no container
WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
