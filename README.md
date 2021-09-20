# Ceres Image Getter 
## Prerequisites:
- Python: >=3.7
- NPM/NPX: >= 6.13.4
- Yarn: 1.22.4
## Frameworks and Libraries Used:
- React JS:
	- Axios
- Python Flask:
	- Zipfile
	- Boto3

##  How to Install:
### Frontend:
1. Ensure port 3000 is unoccupied 
2. Navigate to the ceres-frontend directory
3.  Enter "yarn install"
4.  Enter "yarn start"
5.  The server should start on port 3000
6. When necessary, type ctrl+c to end the server
### Backend:
1. Ensure port 3334 is unoccupied
2. Navigate to the ceres-backend directory
3. Enter "python3.7 -m venv env" to create a virtual environment
4. Enter "source env/bin/activate" to activate it
5. Enter "pip3 install -r requirements.txt" to install requirements
6. Enter "python3.7 image_api.py" to run server on port 3334
7. When necessary, type ctrl+c to end the server

Congratulations! The app should be running

##### Note: Generating the zip file may take a few seconds