# Gender Tracker
Do you have....Gender<sup>TM</sup> Feelings? Do you want a place to store those feelings and see them visuzalized over time? Well this app can sort of kind of do that.

This is a basic app meant to help me and some friends to keep track of gender feelings. It was also a way for me to play around with Vue.js and TailwindCSS.

# Installation

## Prerequisites
Gender Tracker dependes on a postgres database server being accessible. Within the server setup a database for this app along with a user and password. For sake of this readme I will call the database GT, the user GUser, and the password GPass. 

## From Source
If you want to install this from source follow these steps

 1. Clone and move into this repository
 ```bash
git clone https://github.com/tboudreaux/genderTracker
cd genderTracker
```
 2. make a copy of config.py.user
 ```bash
cp genderTracker/config.py.user genderTracker/config.py
```
 3. Setup your database name, username, password, and IP address in config.py (the file is templated so you should only have to change a few value)
 4. Set the Enviroment Variable 'genderTracker_NEW_USER_SECRET' to some value. This will be used to setup the first and admin user.
 5. Run the flask app
 ```bash
python app.py
```
 6. Issue an POST request to register the first user using the following prototype command
 ```bash
curl -X POST <SERVERIP>:<SEVERPORT>/api/user/enroll_user/secret -H "Content-Type: application/json" -d '{"new_user_secret": "$genderTracker_NEW_USER_SECRET", "new_user": "<USERNAME>", "new_pass": "<PASSWORD>", "new_email": "<EMAIL>"}' 
```
 7. Now you can visit localhost:5000 (assuming you are on the same computer you are running this on).

 Note that I have flask setup to listen to 0.0.0.0 for development on my sever which is bad practice for security I belive. 

## From Docker
There is a docker file in the repository. You should be able to run that and be all set.


# Future Things
I want to add more visualizations to this. I also want to add the ability to view how visualizations have evolved over time. Any further suggestions are welcomed!
