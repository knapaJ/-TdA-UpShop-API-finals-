# [TdA Finals] UpShop API

This is the API used in the Tour de App frontend contest.

## Quick Start

To run the current version of the API (version 2) you need:
 - Python 3.10
 - Current version of pipenv

To prepare the development environment you will need to run the following commands:
1) `pipenv update` to install all needed dependencies in to a virtual enviroment.
2) `pipenv shell` to open a shell in the virtual enviroment. (On windows this might fail because of PowerShells external code execution policy)
3) `flask -A apiv2 createdb` to create SQLite database and instance specific info.
4) `flask -A apiv2 run` to run the api on a development server.
   1) Default access tokens are `dev` for the admin (aka, can use all endpoints) and `dev-user` for the user endpoint (aka the endpoints for the contestants)
5) to reset the database you can run `flask -A apiv2 dropdb`. Don't forget to create it again.
6) To test if the server is running the endpoint `/hello-world` is available with all the basic information about the running instance.


If you wish to remove the virtual environment you can run the command `pipenv --rm` in the folder with the environment.
