#!/bin/bash
/home/berto/bot/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8443 --ssl-keyfile /home/berto/bot/uvicorn.key --ssl-certfile /home/berto/bot/uvicorn.crt --reload --workers=1