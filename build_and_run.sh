#!/bin/bash
app="polish_grocer"
docker build -t ${app} .
docker run -d -p 80:80 \
  -e MODULE_NAME="app.main" \
  -e VARIABLE_NAME="app" \
  --name=${app} ${app}
