#!/bin/bash
app="polish_grocer"

# Remove revious versions
docker stop ${app}
docker rm ${app}
docker rmi ${app}

# build new ones 
docker build -t ${app} .
docker run -d -p 80:80 \
  -e MODULE_NAME="app.main" \
  -e VARIABLE_NAME="app" \
  --name=${app} ${app}
