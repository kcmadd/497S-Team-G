# Post Creation Microservice

## Developer

Name: Janvi Tanniru

Email: jtanniru@umass.edu

---
## Overview 
The post creation microservice allows users to put their places up as a listing. This service allows the sublessor to create a posting by providing information about their property such as a brief description about their place along with facilities, number of rooms available to sublet, the price of the listing, the location and duration of the sublet. All this property information is then added to the data source. 

---

## API end-points 


### HTTP methods

1. POST
    * **Route:** /createpost
    * **Description:** This endpoint for a sublessor to create a posting for a lease. Each json which represents a newly created posting is added to a list to be stored in memory.
    * **Expected Data format sent:**
        ```json
        [{
        "pid": str, 
        "posting": { 
            "description": str, 
            "num_rooms_available": int,
            "price": float,
            "location": str,
            "duration": str
            }
        },...]
        ```
    * **Status_Code:** 
        * 201 - when a posting is successfully created 


      
2. GET
    * **Route:** /viewpost/{postid}
    * **Description:** This endpoint to view a particular post based on postid 
    * **Status_Code:** 
        * 200 - when a response is successfull
        * 404 - when a response is unsuccessful


