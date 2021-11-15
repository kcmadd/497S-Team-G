#! /bin/bash

docker run --rm --name my_signup_login -v "$(pwd):/usr/src/app" -p 5007:5007 signup_login_dev
