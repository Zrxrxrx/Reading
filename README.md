# FocusReads
## Introduction
This project is a simple book recommendation system

# Installation and Prerequisites 
The users can run our website and services locally.

Required Software:
- Python version: Python 3.6 - 3.9
- Node.js v16.14.0
- git

Note: An internet connection is required to download both Python modules and Node.js libraries.

# Run on the local environment
### Download and Initialization
- Clone the code on your local environment
- Install python in your local environment
- Install Node.js in your local environment

### Install & Run backend service
- Using terminal to enter directory `backend/`
- Install all required packages: `pip3 install -r requirements.txt`
- Run service: `python3 app.py`

After the backend service runs successfully, then can start the frontend part.

Note: The backend will default to port 5000. If this port is in use it will automatically assign a different unused port. The backend URL needs to be updated in `/frontend/focusreads-app/vue.config.js` before you can start the frontend.

### Install & Run frontend service
- Using terminal to enter directory `frontend/focusreads-app`
- Using `npm i` to install the frontend related frameworks and dependencies.
- Run frontend using `npm run serve`

Go to http://localhost:8080

If the frontend port is in use, the frontend should attempt to use another unused port. The new port needs to be updated in the `/frontend/focusreads-app/src/main.js` file.

# Note for Site Owner
The project comes with a default administrator user with the following credentials:

| Email           | Password |
| -----           | -------- |
| admin@admin.com | iamadmin |

Additional administrator users can only be added through the database manually (this is done to ensure the integrity of the site in the case of the breach of an administrator account).

