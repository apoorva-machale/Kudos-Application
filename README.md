Install docker and IDE
Build docker container - docker build -t kudos_app .
Run container - docker run --name fastapi-container -d -p 3000:3000 kudos_app
look for apis in the browser - http://localhost:3000/docs/