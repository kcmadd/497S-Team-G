# Query Service

### Developer

Janvi Tanniru, Aditya Narayanan

jtanniru@umass.edu, arnarayanan@umass.edu

### Service Overview

The event bus manages events and decouples microservcies to make the service scalable. 


### API Endpoints

* POST: /events
This event receives the POST requests made by all services and commuicates an event to all the running microservcies. The other services, POST_SERVICE, SIGNUP_LOGIN, and REQUEST_INFO get information that an event has been created. The QUERY_SERIVICE parses the body sent by the event bus with a type, and pushes data into the DB. The event bus manages the events of the platform

### Steps to build the service

1. Technologies: Python
2. Using the terminal:

```sh
cd Event_Bus
pip3 install pdm
pdm install
pdm run start_server
```


