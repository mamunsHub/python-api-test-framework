### Pre-reqs:
Python3 needs to be installed in the PC.


### For this framework some third party free people-api endpoints will be used
### That API project needs to up and running in your local server to make requests

--------------------------------------------------------------------------------------------------------------

## To setup clone people-api repo from github, cd to the newly cloned repo and then activate the pipenv by running below commands:

git clone https://github.com/automationhacks/people-api.git
cd people-api
pipenv shell
pipenv install
python build_database.py
python server.py

---------------------------------------------------------------------------------------------------------------

### To Setup the Framework:
clone the repo first - git clone 
cd python-api-test-framework

### Create Virtual Environment
pip install virtualenv
python -m venv .venv

### Activate Virtual Environment
.venv\Scripts\activate.bat

### Install all the dependencies
pip install -r requirements.txt