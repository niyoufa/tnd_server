#!/bin/sh
cd /usr/share/nginx/renren
git pull origin dev
supervisorctl restart all