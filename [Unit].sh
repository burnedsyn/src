[Unit]
Description=start Europai
After=network.target

[Service]
User=europai
WorkingDirectory=/home/europai/src
ExecStart=/bin/bash /home/europai/src/start.sh
Restart=always
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=Europai

[Install]
WantedBy=multi-user.target