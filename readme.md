# Table of Contents
1. [Project description](#project-description)
2. [Technologies and tools](#technologies-and-tools)
3. [Run project and tests](#run-project-and-tests)
4. [Run Jenkins pipeline](#run-jenkins-pipeline)
5. [Main functionalities](#main-functionalities)


## Project description
**crypto_portfolio_service_REST_API** - REST API for user cryptocurrency portfolio management. 
Works with an external API that allows you to download the latest data related with 
selected cryptocurrency, which is then processed by the API implemented in scope of 
this project. All cryptocurrencies and related data can be stored in selected user portfolio. 
All users, cryptocurrencies and portfolios objects are stored in PostgreSQL database.


## Technologies and tools

- Python
- Django
- Django Rest Framework
- DRF Spectacular
- Docker
- Jenkins
- Vagrant
- PostgreSQL
- PyCoinGecko
- PreCommit
- Flake8
- Black

## Run project and tests

Follow listed steps to start project using docker container:
1. Go to `<your_path_to_project>/crypto_portfolio_service_REST_API`
2. Build docker containers `docker build .`
3. Run docker containers `docker compose up` -> Now development server is up
4. Run interactive REST API documentation (DRF Swagger), enter in your browser `http://0.0.0.0:8000/api/docs`

Follow listed steps to execute tests (development server must be running):
1. Open second window in terminal.
2. Check running containers id's `docker ps`
3. Enter application container `docker exec -it <container_id> /bin/bash`
4. Go to main project folder `cd crypto_portfolio_service_REST_API`
5. Execute tests related with user `python manage.py test user.tests`
6. Execute tests related with cryptocurrency portfolio service `python manage.py test crypto_service.tests`


## Run Jenkins pipeline

Content of Jenkins pipeline:
1. Clone project from GitHub
2. Requirements installation
3. Code analysis by Flake8
4. Run app in Docker container
5. Execute tests
6. Cleanup

Follow listed steps to run Jenkins pipeline:
1. Automatically install and configure virtual machine using **ci/Vagrantfile** `vagrant up`
2. Connect with created virtual machine using ssh `vagrant ssh`
3. Change Jenkins privileges - add `jenkins ALL=(ALL) NOPASSWD: ALL` at the end of `/etc/sudoers` file
4. Connect with Jenkins using browser and configured internal network IP and Jenkins port, for example `192.168.33.20:8080`
5. Create pipeline using content of `ci/Jenkinsfile`

![image](https://github.com/grzesiekszymanski/crypto_portfolio_service_REST_API/assets/80125719/bd1325cd-86d2-423d-9fe1-1a1f80d9022f)



## Main functionalities

### User app:
- Users authentication
- Users management
- Superusers management
- Data serialization
- Tests

### Crypto portfolio app:
- Separated portfolio for each user
- Single cryptocurrency management
  - Getting live time price
  - Worth recalculation
  - Getting 24h ago price value
  - Calculating every single coin participation in portfolio
- General portfolio data
  - Recalculations after every portfolio update
    - Total value
    - Total profit/loss in USD
    - Total profit/loss in percent
    - Total profit/loss in USD compared with 24h ago
    - Total profit/loss in percent compared with 24h ago
- Listing thousands of available cryptocurrencies on exchanges 
- Tests for all functionalities

### Other:
- Users, Cryptocurrencies and Portfolios maintained in PostgreSQL database
- Containerization (Docker)
- Interactive REST API documentation (DRF Swagger)
- Code management (PreCommit, Flake8, Black)
