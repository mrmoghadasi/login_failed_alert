#!/bin/bash


mkdir /usr/lib/ssh-failed
cp ssh-failed.py /usr/lib/ssh-failed/ssh-failed-login.py
cp config.sample.ini /usr/lib/ssh-failed/config.ini


echo '[Unit]
Description=SSH Failed Login Detection
After=network.target

[Service]
User=root
Group=root
Type=simple
Restart=always
RestartSec=5s
ExecStart=/usr/bin/python3 /usr/lib/ssh-failed/ssh-failed-login.py

[Install]
WantedBy=multi-user.target' > /etc/systemd/system/ssh-failed-login.service


sudo systemctl daemon-reload
sudo systemctl start ssh-failed-login.service
sudo systemctl status ssh-failed-login.service
sudo systemctl enable ssh-failed-login.service




