# flaskblog #
## Here is a blog built using flask version 3.03 ##


## Here is how you install flaskblog in Visual Studio Code. ##

1. Clone the project
2. Open the flaskblog folder in VSC.
3. Create the environment variables. To create the virtiual env follow 
this link [https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/] .
4. Run "$env:FLASK_ENV='dev'" then create the db by following the link here [https://flask-migrate.readthedocs.io/en/latest/]. 
Before using flask migrate use $env:FLASK_ENV='dev' in powershell. 
5. To run the code in the CLI follow this link [https://flask.palletsprojects.com/en/2.3.x/cli/] . 

For example on windows and powershell in VSC type 

> $env:FLASK_DEBUG='True'              
> $env:FLASK_ENV='dev'
> flask --app app run or flask run

6. To run pytest on windows and powershell in VSC type    
> $env:FLASK_ENV='test'      
> pytest -q --capture=no  

## There are a few bugs and minor errors. I am fixing them and I cleaning up the code I also need to add css and improve the html. ##