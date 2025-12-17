# Usar imagem base leve do Python 3.10
FROM python:3.10-slim

# Definir diretório de trabalho
WORKDIR /app

# Variáveis de ambiente para Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Instalar dependências do sistema necessárias para compilação e libs
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar apenas requirements.txt primeiro (para cache do Docker)
COPY requirements.txt .

# Atualizar pip e instalar dependências
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar todo o código fonte
COPY . .

# Expor a porta 8000
EXPOSE 8000

# Comando de execução (substitui o script manual)
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
