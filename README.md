# PythonOOP Project

Made by Raul Birsan with Augustin Sasu.

## Build the app:

docker-compose -f docker-compose.dev.yml up --build  

### Access Swagger UI to see and use the operations:

http://localhost:8000/docs

### Access RabbitMQ Management to see the queue of messages sent to Rabbit:

http://localhost:15672/

Use guest:guest

## View the logs made by log_consumer:

docker exec -it log_consumer cat /var/log/my_app.log  

## Enter in the math-api container bash to see the entries made in the SQLLite database:

docker exec -it math-api bash 

### Enter sqlite3 CLI
sqlite3 persistent-db/db.sqlite

.tables 

SELECT * FROM math_request;

