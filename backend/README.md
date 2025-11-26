# Backend - Renum Platform

API FastAPI com autenticação Supabase.

## Desenvolvimento

```bash
cd backend
python -m venv venv
venv\Scripts\Activate.ps1  # Windows
pip install -r requirements.txt
python -m src.main
```

O backend rodará em `http://localhost:8000`

## Documentação API

Acesse `http://localhost:8000/docs` para ver a documentação Swagger interativa.

## Estrutura

- `src/` - Código fonte
- `src/api/` - Rotas e endpoints
- `src/services/` - Lógica de negócio
- `src/models/` - Modelos Pydantic
- `src/config/` - Configurações
- `src/utils/` - Utilitários

## Deploy

Deploy manual para VPS.

## Tecnologias

- Python 3.11+
- FastAPI
- Supabase
- Pydantic
- Uvicorn
- Loguru
