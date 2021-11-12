# Signup and Login Service

### Developer

Kalyan Maddineni

smaddineni@umass.edu

### Service Overview

The goal of this microservice is to allow users to signup and login to their accounts as well as provide the correct user permissions . 

### API Endpoints

#### HTTP Methods

1. GET 
    * Endpoint name: /login
    * This endpoint is used to login to user account
    
2. POST
    * Endpoint name: /signup
    * This endpoint is used to signup(create) a new user account

#### Data Format Sent

* POST Request
```json
[
    {
    "username": str,
    "password": {
    "fname": str,
    "lname": str,
    "phone": str,
    },
]
```
