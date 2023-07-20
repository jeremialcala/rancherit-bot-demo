#!/bin/bash
gh repo clone jeremialcala/rancherit-bot-demo
cd rancherit-bot-demo/ || exit
git checkout develop
git pull

docker rm -f rancherit-bot-demo
docker rmi rancherit-bot-demo
docker system prune -a -f
docker build -t rancherit-bot-demo:latest .
docker run --env-file=env_variables -it -p 8080:8080 --name rancherit-bot-demo -d rancherit-bot-demo
