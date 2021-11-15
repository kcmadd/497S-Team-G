#! /bin/bash
open -a Docker.app

cd SIGNUP_LOGIN
pdm run docker_build
pdm run docker_run

cd ../POSTS_SERVICE_API
pdm run docker_build
pdm run docker_run

cd ../Query_Service
pdm run docker_build
pdm run docker_run

cd ../Request_Info_API
pdm run docker_build
pdm run docker_run

cd ../View_Posts_Service
pdm run docker_build
pdm run docker_run

cd ../Event_Bus
pdm run docker_build
pdm run docker_run

cd ../Database_Service
pdm run docker_compose_db