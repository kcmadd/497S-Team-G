# Query Service

### Developer

Aditya Narayanan

arnarayanan@umass.edu

### Service Overview

Setting up the MongoDB database

### Steps to setup the Mongo DB Database (MacOS)
0. Install Homebrew via https://docs.brew.sh/Installation
1. brew tap mongodb/brew
2. brew install mongodb-community@5.0
3. brew services start mongodb-community@5.0
4. Open a new terminal and run the command *mongo* . You should be in the mongo shell now
5. Run *use posts*
6. Then run *db.createCollection(“posts_collection”)*
7. Run *use user_info*
8. Then run *db.createCollection(“user_collection”)*