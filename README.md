# Renum Platform

Monorepo para plataforma Renum - Sistema de agentes de IA com frontend e backend.

## 📁 Estrutura

- `frontend/` - Aplicação React (Vite + TypeScript + Tailwind) - Deploy Vercel
- `backend/` - API FastAPI (Python) - Deploy VPS
- `docs/` - Documentação e credenciais
- `.kiro/` - Specs e steering para desenvolvimento com IA

## 🚀 Desenvolvimento

### Frontend
```bash
cd frontend
npm install
npm run dev
```
Acesse: `http://localhost:5173`

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\Activate.ps1  # Windows
pip install -r requirements.txt
python -m src.main
```
Acesse: `http://localhost:8000`
Docs: `http://localhost:8000/docs`

## 📚 Documentação

Ver README em cada diretório para mais detalhes:
- [Frontend README](frontend/README.md)
- [Backend README](backend/README.md)

## 🔐 Credenciais

Credenciais sensíveis estão em `docs/` (não commitadas no Git).

## 🌐 Deploy

- **Frontend:** Vercel (automático via Git)
- **Backend:** VPS manual

## 👤 Login Padrão

- **Email:** admin@renum.tech
- **Senha:** Admin@123456
