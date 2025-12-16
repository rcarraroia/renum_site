#!/bin/bash
# Setup Renum API Service
# Run as root

echo "=========================================="
echo "RENUM API SETUP"
echo "=========================================="

# 1. Update & Install Python
apt-get update
apt-get install -y python3-venv python3-pip git

# 2. Setup Directory
mkdir -p /home/renum/backend
cd /home/renum

# 3. Pull Code (Assumes public or keys setup, if fails, manual pull needed)
if [ ! -d "renum_site" ]; then
    echo "Cloning repository..."
    git clone https://github.com/rcarraroia/renum_site.git
else
    echo "Repository exists, pulling latest..."
    cd renum_site
    git pull
    cd ..
fi

# Link backend
rm -rf /home/renum/backend
ln -s /home/renum/renum_site/backend /home/renum/backend

# 4. Setup Venv
echo "Setting up Virtualenv..."
cd /home/renum/backend
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 5. Create Systemd Service
echo "Creating Systemd Service..."
cat > /etc/systemd/system/renum-api.service <<EOF
[Unit]
Description=RENUM API
After=network.target

[Service]
User=root
WorkingDirectory=/home/renum/backend
Environment="PATH=/home/renum/backend/venv/bin"
EnvironmentFile=/home/renum/backend/.env
ExecStart=/home/renum/backend/venv/bin/uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# 6. Start Service
systemctl daemon-reload
systemctl enable renum-api
systemctl restart renum-api

echo "✅ API Setup Complete. Check status with: systemctl status renum-api"
