# ==================================
# RENUM - VPS Deploy Script (Docker)
# ==================================

#!/bin/bash
set -e

echo "=========================================="
echo "RENUM DEPLOYMENT - DOCKER VERSION"
echo "=========================================="

# 1. Instalar Docker
echo "📦 Instalando Docker..."
apt-get update
apt-get install -y ca-certificates curl gnupg
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
chmod a+r /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  tee /etc/apt/sources.list.d/docker.list > /dev/null

apt-get update
apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# 2. Instalar Certbot
echo "🔒 Instalando Certbot..."
apt-get install -y certbot

# 3. Clonar Repositório
echo "📥 Clonando repositório..."
cd /home
if [ -d "renum_site" ]; then
    cd renum_site
    git pull
else
    git clone https://github.com/rcarraroia/renum_site.git
    cd renum_site
fi

# 4. Configurar .env
echo "⚙️ Configurando variáveis de ambiente..."
if [ ! -f "backend/.env" ]; then
    echo "❌ ERRO: Arquivo backend/.env não encontrado!"
    echo "📝 Crie o arquivo backend/.env com as variáveis necessárias"
    exit 1
fi

# 5. Obter Certificado SSL (primeira vez)
echo "🔐 Obtendo certificado SSL..."
if [ ! -d "/etc/letsencrypt/live/api.renum.com.br" ]; then
    certbot certonly --standalone -d api.renum.com.br \
        --non-interactive --agree-tos -m rcarraro2015@gmail.com
else
    echo "✅ Certificado já existe"
fi

# 6. Build e Start Containers
echo "🐳 Iniciando containers Docker..."
docker compose down || true
docker compose build --no-cache
docker compose up -d

# 7. Aguardar containers iniciarem
echo "⏳ Aguardando containers..."
sleep 15

# 8. Verificar Status
echo "📊 Status dos containers:"
docker compose ps

echo ""
echo "✅ DEPLOYMENT CONCLUÍDO!"
echo ""
echo "🌐 API: https://api.renum.com.br"
echo "📊 Health: https://api.renum.com.br/health"
echo "📖 Docs: https://api.renum.com.br/docs"
echo ""
echo "📝 Comandos Úteis:"
echo "  docker compose logs -f        # Ver logs"
echo "  docker compose ps             # Status"
echo "  docker compose restart api    # Reiniciar API"
echo "  docker compose down           # Parar tudo"
echo "  docker compose up -d          # Iniciar tudo"
echo ""
