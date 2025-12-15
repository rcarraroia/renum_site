#!/bin/bash
# Setup Redis and Celery on VPS
# Sprint 07A - Integrações Core

echo "============================================================"
echo "SPRINT 07A - VPS SETUP (Redis + Celery)"
echo "============================================================"

# 1. Install Redis
echo ""
echo "📦 Installing Redis..."
sudo apt update
sudo apt install -y redis-server

# 2. Configure Redis to start on boot
echo ""
echo "🔧 Configuring Redis..."
sudo systemctl enable redis-server
sudo systemctl start redis-server

# 3. Verify Redis is running
echo ""
echo "✅ Verifying Redis..."
sudo systemctl status redis-server --no-pager

# 4. Test Redis connection
echo ""
echo "🧪 Testing Redis connection..."
redis-cli ping

# 5. Create Celery Worker systemd service
echo ""
echo "📝 Creating Celery Worker service..."
sudo tee /etc/systemd/system/renum-celery.service > /dev/null <<EOF
[Unit]
Description=RENUM Celery Worker
After=network.target redis-server.service

[Service]
Type=forking
User=root
Group=root
WorkingDirectory=/home/renum/backend
Environment="PATH=/home/renum/backend/venv/bin"
ExecStart=/home/renum/backend/venv/bin/celery -A src.workers.celery_app worker --loglevel=info --logfile=/home/renum/logs/celery-worker.log --pidfile=/var/run/celery/worker.pid --detach
ExecStop=/bin/kill -s TERM \$MAINPID
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# 6. Create Celery Beat systemd service
echo ""
echo "📝 Creating Celery Beat service..."
sudo tee /etc/systemd/system/renum-celery-beat.service > /dev/null <<EOF
[Unit]
Description=RENUM Celery Beat Scheduler
After=network.target redis-server.service

[Service]
Type=forking
User=root
Group=root
WorkingDirectory=/home/renum/backend
Environment="PATH=/home/renum/backend/venv/bin"
ExecStart=/home/renum/backend/venv/bin/celery -A src.workers.celery_app beat --loglevel=info --logfile=/home/renum/logs/celery-beat.log --pidfile=/var/run/celery/beat.pid --detach
ExecStop=/bin/kill -s TERM \$MAINPID
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# 7. Create PID directory for Celery
echo ""
echo "📁 Creating Celery PID directory..."
sudo mkdir -p /var/run/celery
sudo chown root:root /var/run/celery

# 8. Create logs directory
echo ""
echo "📁 Creating logs directory..."
sudo mkdir -p /home/renum/logs
sudo chown root:root /home/renum/logs

# 9. Reload systemd
echo ""
echo "🔄 Reloading systemd..."
sudo systemctl daemon-reload

# 10. Enable services
echo ""
echo "✅ Enabling services..."
sudo systemctl enable renum-celery.service
sudo systemctl enable renum-celery-beat.service

# 11. Start services
echo ""
echo "🚀 Starting services..."
sudo systemctl start renum-celery.service
sudo systemctl start renum-celery-beat.service

# 12. Check status
echo ""
echo "📊 Service Status:"
echo ""
echo "Redis:"
sudo systemctl status redis-server --no-pager | head -n 5
echo ""
echo "Celery Worker:"
sudo systemctl status renum-celery --no-pager | head -n 5
echo ""
echo "Celery Beat:"
sudo systemctl status renum-celery-beat --no-pager | head -n 5

echo ""
echo "============================================================"
echo "✅ SETUP COMPLETED"
echo "============================================================"
echo ""
echo "📋 Next Steps:"
echo "1. Update /home/renum/backend/.env with REDIS_URL and ENCRYPTION_KEY"
echo "2. Restart backend: sudo systemctl restart renum-api"
echo "3. Monitor logs:"
echo "   - Celery Worker: tail -f /home/renum/logs/celery-worker.log"
echo "   - Celery Beat: tail -f /home/renum/logs/celery-beat.log"
echo ""
