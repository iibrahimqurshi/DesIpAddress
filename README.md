
<!-- Clone the project -->
Follow this commands:
git clone 'URL'


<!-- Run Backend - in new terminal-->
# 1-Go to Backend DIR
cd ./Backend
# 2-Install the requirements
pip install -r requirement.txt
# 3-install pipenv
pip install pipenv
# 4-Update Python
python -m pip install --upgrade python
# 5-Update pip
python -m pip install --upgrade pip
# 6-Create a virtual environment and activate it
pipenv shell
# 7-install the requirement in the enviroment
pipenv install -r requirement.txt
# 8-Start the server
uvicorn main:app --reload



<!-- RUN Frontend - in new terminal-->
# Go to Frontend Dir
cd ./Frontend
cd ./my-app

# install the Node Modules
npm install

# Run the app 
npm start






