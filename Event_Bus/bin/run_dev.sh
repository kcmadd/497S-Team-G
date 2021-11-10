#! /bin/bash

docker run --rm --name my_event_bus_microservice -v "$(pwd):/usr/src/app" -p 5005:5005 event_bus_microservice_dev
