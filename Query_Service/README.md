# Query Service

### Developer

Aditya Narayanan

arnarayanan@umass.edu

### Service Overview

The goal of the query service is to query particular information from the data source based on certain filters or constraints. The service will also be used to add information to the data source which inlcudes adding a list of users who are interested in a posting. 

### API Endpoints

#### HTTP Methods

1. GET 
    * Endpoint name: /location_filter/{location}
    * This endpoint is used to filter posts by location (say: Amherst)
    * Status_Code: 200 when a GET request is successful. When unsuccessful, status_code: 404 showing that the resource does not exist

2. POST
    * Endpoint name: /mark_interested
    * This endpoint adds user ID's to a list of users interested in a property/listing
    * Status_Code: 201 when a post is succesfully sent.

#### Data Format Sent

* POST Request
```json
[
    {
    "pid": str,
    "posting": {
    "description": str,
    "num_rooms": int,
    "price": float,
    "location": str
    },
    "interested_users": list
}
]
```
##### HTTP Status Codes

* Status_Code 201 (Success)

* Status_Code 404 (Error)