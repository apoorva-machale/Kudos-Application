Backend
Install docker and IDE
Build docker container - docker build -t kudos_app .
Run container - docker run --name fastapi-container -d -p 3000:3000 kudos_app
look for apis in the browser - http://localhost:3000/docs/
# (Activate your virtual environment)
uvicorn main:app --reload


Frontend
npm install vite@4.5.0 --save-dev
npm create vite@latest kudos-frontend -- --template react
cd kudos-frontend
npm install
npm run dev
