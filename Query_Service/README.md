# Query Service

### Developer

Aditya Narayanan

arnarayanan@umass.edu

### Service Overview

The goal of the query service is to interact with the database. The query service gets the data from the event bus and modifies the database. 

### API Endpoints

#### HTTP Methods

* POST: '/events'
This endpoint is used to parse data sent from the event bus to this service. Depedning on the message type sent, this service will push/modify data in the database by collection. 

#### Data Format

* POST Request
```json
{
    "type": str,
    "data": {
        values here can be another json containing user or post information
    }
}
```
##### HTTP Status Codes

* Status_Code 201 (Success)

* Status_Code 404 (Error)

### Messages Sent and Received by Event Bus

* **Packet 1**
**Event Type**: Post_Created
**Payload**: 
```json
{
"type": "Post_Created",
"data": {
"uid": str, 
"pid": str, 
"posting" : {
    "amenities" : str, 
    "num_rooms_availables" : int, 
    "price" : float, 
    "Restrictions": str,  (#ex: no pets, no smoking, couples only students)
    "lease_duration": str,
    "street_address" : str, 
    "city": str,
    "state": str, 
    "country": str
    }
}
```

* **Packet 2**
**Event Type**: User_Created
**payload**:
```json
{
    "type": "User_Created",
    "data": 
    {
    "user_id": str,
    "username": str,
    "password": str,
    "fname": str,
    "lname": str,
    "phone": str
    }
}
```

* **Packet3**
**Event_Type**: Mark_Interested
**payload**:
```json
{
    "type": "Mark_Interested",
    "data": {
    "postId": str,
    "uid": str,
    "fname": str,
    "lname": str,
    "email": str, 
    "phone": str
    }
}
```

* **Packet4**
**Event_Type**: Mark_Not_Interested
**payload**:
```json
{
    "type": "Mark_Not_Interested",
    "data": {
    "postId": str,
    "uid": str
    }
}
``` 

### Steps to Build the Service

1. Technologies to be Installed: Python
2. Using the terminal, do the following:

```sh
cd Query_Service
pip3 install pdm
pdm install
pdm run start_server
```