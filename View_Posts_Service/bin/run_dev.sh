#! /bin/bash

docker run --rm --name my_view_posts_microservice -v "$(pwd):/usr/src/app" -p 5000:5000 view_posts_microservice_dev
