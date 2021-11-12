#! /bin/bash

docker run --rm --name my_signup_login -v "$(pwd):/usr/src/app" -p 8080:8080 signup_login_dev
