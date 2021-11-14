#! /bin/bash

docker run --rm --name my_query_service_dev -v "$(pwd):/usr/src/app" -p 5003:5003 query_service_dev
