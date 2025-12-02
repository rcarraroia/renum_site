# 🖥️ Guia de Acesso à VPS - RENUM

## Informações Gerais

**Provedor:** [Nome do Provedor - ex: DigitalOcean, AWS, Contabo]  
**Sistema Operacional:** Ubuntu 22.04 LTS (ou conforme instalado)  
**Região:** [Região do servidor]  

---

## 📋 Credenciais de Acesso

⚠️ **IMPORTANTE:** Mantenha estas informações seguras e nunca as compartilhe publicamente

### Acesso SSH

**IP do Servidor:**
```
72.60.151.78
```

**Porta SSH:**
```
22
```

**Usuário:**
```
root
```

**Método de Autenticação:**
- [x] Senha (configurar chave SSH é recomendado)
- [ ] Chave SSH (recomendado para produção)

---

## 🔑 Conexão SSH

### Usando Senha

```bash
ssh root@72.60.151.78
# Digite a senha quando solicitado
```

### Usando Chave SSH (Recomendado)

```bash
# Gerar chave SSH (se ainda não tiver)
ssh-keygen -t ed25519 -C "renum-vps"

# Copiar chave para servidor
ssh-copy-id -i ~/.ssh/id_ed25519.pub root@72.60.151.78

# Conectar
ssh -i ~/.ssh/id_ed25519 root@72.60.151.78
```

### Configurar Alias SSH (Opcional)

Edite `~/.ssh/config`:

```
Host renum-vps
    HostName 72.60.151.78
    User root
    Port 22
    IdentityFile ~/.ssh/id_ed25519
```

Depois conecte simplesmente com:
```bash
ssh renum-vps
```

---

## 🗂️ Estrutura de Diretórios

```
/home/renum/
├── backend/                 # Código do backend
│   ├── src/
│   ├── .env                # Variáveis de ambiente
│   ├── requirements.txt
│   └── ...
├── logs/                   # Logs da aplicação
│   ├── fastapi.log
│   ├── celery.log
│   └── nginx.log
├── backups/                # Backups locais
└── scripts/                # Scripts de manutenção
```

---

## 🚀 Serviços Instalados

### FastAPI (Backend)

**Gerenciamento:**
```bash
# Status
sudo systemctl status renum-api

# Iniciar
sudo systemctl start renum-api

# Parar
sudo systemctl stop renum-api

# Reiniciar
sudo systemctl restart renum-api

# Ver logs
sudo journalctl -u renum-api -f
```

**Arquivo de Serviço:** `/etc/systemd/system/renum-api.service`

### Celery Worker

**Gerenciamento:**
```bash
# Status
sudo systemctl status renum-celery

# Iniciar
sudo systemctl start renum-celery

# Parar
sudo systemctl stop renum-celery

# Reiniciar
sudo systemctl restart renum-celery

# Ver logs
sudo journalctl -u renum-celery -f
```

**Arquivo de Serviço:** `/etc/systemd/system/renum-celery.service`

### Redis

**Gerenciamento:**
```bash
# Status
sudo systemctl status redis

# Iniciar
sudo systemctl start redis

# Parar
sudo systemctl stop redis

# Reiniciar
sudo systemctl restart redis

# Acessar CLI
redis-cli
```

### Nginx (Proxy Reverso)

**Gerenciamento:**
```bash
# Status
sudo systemctl status nginx

# Iniciar
sudo systemctl start nginx

# Parar
sudo systemctl stop nginx

# Reiniciar
sudo systemctl restart nginx

# Recarregar configuração
sudo nginx -s reload

# Testar configuração
sudo nginx -t
```

**Arquivo de Configuração:** `/etc/nginx/sites-available/renum`

---

## 🔧 Comandos Úteis

### Atualizar Código

```bash
cd /home/renum/backend
git pull origin main
pip install -r requirements.txt
sudo systemctl restart renum-api
sudo systemctl restart renum-celery
```

### Ver Logs em Tempo Real

```bash
# FastAPI
tail -f /home/renum/logs/fastapi.log

# Celery
tail -f /home/renum/logs/celery.log

# Nginx
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log

# Todos os serviços
sudo journalctl -f
```

### Monitorar Recursos

```bash
# CPU e Memória
htop

# Espaço em disco
df -h

# Uso de disco por diretório
du -sh /home/renum/*

# Processos Python
ps aux | grep python

# Conexões de rede
netstat -tulpn
```

### Backup Manual

```bash
# Criar backup do código
cd /home/renum
tar -czf backups/backend-$(date +%Y%m%d-%H%M%S).tar.gz backend/

# Listar backups
ls -lh backups/
```

---

## 🔒 Segurança

### Firewall (UFW)

```bash
# Status
sudo ufw status

# Permitir SSH
sudo ufw allow 22/tcp

# Permitir HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Habilitar firewall
sudo ufw enable
```

### Fail2Ban (Proteção contra Brute Force)

```bash
# Status
sudo systemctl status fail2ban

# Ver IPs banidos
sudo fail2ban-client status sshd

# Desbanir IP
sudo fail2ban-client set sshd unbanip [IP]
```

### Atualizar Sistema

```bash
# Atualizar lista de pacotes
sudo apt update

# Atualizar pacotes
sudo apt upgrade -y

# Atualizar sistema completo
sudo apt dist-upgrade -y

# Remover pacotes não utilizados
sudo apt autoremove -y
```

---

## 📊 Monitoramento

### Verificar Status Geral

```bash
# Script de status (criar se não existir)
#!/bin/bash
echo "=== Status dos Serviços RENUM ==="
echo ""
echo "FastAPI:"
systemctl is-active renum-api
echo ""
echo "Celery:"
systemctl is-active renum-celery
echo ""
echo "Redis:"
systemctl is-active redis
echo ""
echo "Nginx:"
systemctl is-active nginx
echo ""
echo "=== Uso de Recursos ==="
echo ""
echo "Memória:"
free -h
echo ""
echo "Disco:"
df -h /
echo ""
echo "CPU:"
uptime
```

Salvar como `/home/renum/scripts/status.sh` e executar:
```bash
chmod +x /home/renum/scripts/status.sh
/home/renum/scripts/status.sh
```

---

## 🚨 Troubleshooting

### Serviço não inicia

```bash
# Ver logs detalhados
sudo journalctl -u renum-api -n 100 --no-pager

# Verificar arquivo de serviço
sudo systemctl cat renum-api

# Recarregar configuração
sudo systemctl daemon-reload
sudo systemctl restart renum-api
```

### Erro de Permissão

```bash
# Corrigir permissões
sudo chown -R renum:renum /home/renum/backend
sudo chmod -R 755 /home/renum/backend
```

### Porta já em uso

```bash
# Ver processo usando porta 8000
sudo lsof -i :8000

# Matar processo
sudo kill -9 [PID]
```

### Espaço em disco cheio

```bash
# Limpar logs antigos
sudo journalctl --vacuum-time=7d

# Limpar cache apt
sudo apt clean

# Remover backups antigos
find /home/renum/backups -mtime +30 -delete
```

---

## 🔄 Rotinas de Manutenção

### Diária
- [ ] Verificar logs de erro
- [ ] Monitorar uso de recursos

### Semanal
- [ ] Atualizar pacotes do sistema
- [ ] Verificar backups
- [ ] Revisar logs de segurança

### Mensal
- [ ] Atualizar dependências Python
- [ ] Limpar logs antigos
- [ ] Revisar configurações de segurança
- [ ] Testar restore de backup

---

## 📞 Informações de Suporte

**Provedor VPS:**
- Site: [URL do provedor]
- Suporte: [Email/Telefone]
- Painel: [URL do painel]

**Credenciais do Painel:**
- Usuário: [seu-usuario]
- Senha: [armazenada em gerenciador de senhas]

---

## 📝 Notas Adicionais

### Variáveis de Ambiente

Arquivo: `/home/renum/backend/.env`

```bash
# Editar variáveis
nano /home/renum/backend/.env

# Após editar, reiniciar serviços
sudo systemctl restart renum-api
sudo systemctl restart renum-celery
```

### Certificado SSL (HTTPS)

```bash
# Instalar Certbot
sudo apt install certbot python3-certbot-nginx

# Obter certificado
sudo certbot --nginx -d seu-dominio.com

# Renovar automaticamente (já configurado)
sudo certbot renew --dry-run
```

---

**Última atualização:** 2025-11-25  
**Responsável:** Equipe RENUM  
**Versão:** 1.0
