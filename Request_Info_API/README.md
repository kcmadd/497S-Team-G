# Request Info Microservice

## Developer

Name: Harshal Dhelia

Email: hdhelia@umass.edu

---
## Overview 
The Request Info microservice will allow logged in subletters to get information about the sublessor who has put out a post that the subletter is interested in. 

---

## API end-points 


### HTTP methods

1. POST
    * **Route:** /posts/{postId}
    * **Description:** This endpoint sends the subletters information to the sublessor.
    * **Expected Data format sent:**
        ```json
        {
            "user_name": str, 
            "phone_number": str
        }
        ```
    * **Status_Code:** 
        * 200 when the subletters information is sent successfully. 
        * 404 when its unsuccessful. 


      
2. GET
    * **Route:** /posts/{postid}
    * **Description:** This endpoint is to get the owner's information who uploaded the post. 
    * **Status_Code:** 
        * 200 when the sublessor's information is retreived successfully.
        * 404 When its unsuccessful.


