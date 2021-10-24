#! /bin/bash

docker run --rm --name my_python_server_1 -v "$(pwd):/usr/src/app" -p 5000:5000 python_server_1_dev
