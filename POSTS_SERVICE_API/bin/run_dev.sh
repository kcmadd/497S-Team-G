#! /bin/bash

docker run --rm --name my_posts_server_dev -v "$(pwd):/usr/src/app" -p 5000:5000 posts_server_dev
