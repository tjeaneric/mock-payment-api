#!/bin/bash

#migrations
chmod +x ./migrations.sh
./migrations.sh

exec uvicorn  main:app --host 0.0.0.0 --port 8000