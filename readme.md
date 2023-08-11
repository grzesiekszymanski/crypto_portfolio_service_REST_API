# Table of Contents
1. [Project description](#Project-description)
2. [Technologies and tools](#Technologies-and-tools)
3. [Run project and tests](#Run-project-and-tests)
4. [Main functionalities](#Main-functionalities)


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
- PostgreSQL
- Docker
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

Follow listed steps to execute tests:
5. Go to main project folder `cd crypto_portfolio_service_REST_API`
6. Execute tests related with user `python manage.py test user.tests`
7. Execute tests related with cryptocurrency portfolio service `python manage.py test crypto_service.tests`

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
