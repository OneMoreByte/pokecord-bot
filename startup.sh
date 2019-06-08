#!/bin/sh

echo "Starting up bots."

for user in ./users/*; do
	docker run -d --log-driver=json-file -v /storage/code/personal/pokecord-bot/movies:/movies:rw --env-file $user pokecord-bot
    sleep 15
done
