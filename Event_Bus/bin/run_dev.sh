#! /bin/bash

docker run --rm --name my_event_bus_service -v "$(pwd):/usr/src/app" -p 5005:5005 event_bus_service_dev
