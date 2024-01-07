[Unit]
Description= TG Bot MagicCrochet_61
After=syslog.target
After=network.target

[Service]
Type=simple
WorkingDirectory=/home/MagicCrochet_bot/knitting_luda_bot
ExecStart=/usr/bin/python3 /home/MagicCrochet_bot/knitting_luda_bot/bot.py
RestartSec=60
Restart=always

[Install]
WantedBy=multi-user.target