# ku-polls
![GitHub CI](https://github.com/kulisarawiangin/ku-polls/actions/workflows/python-app.yml/badge.svg) [![codecov](https://codecov.io/gh/kulisarawiangin/ku-polls/coverage.svg?branch=master)](https://app.codecov.io/github/kulisarawiangin/ku-polls/tree/master/polls)


Web application for polls and surveys at Kasetsart University
# Online Polls for Kasetsart University
An application for conducting a poll or survey, written in Python using Django. It is based on the [Django Tutorial project](https://docs.djangoproject.com/en/4.1/intro/tutorial01/), with additional functionality.

This application is part of the [Individual Software Process](https://cpske.github.io/ISP/) course at [Kasetsart University](https://ku.ac.th).

# How to Install and Run
install python in your computer

1. Choose path that this project will be in then clone this repository by type this command in your terminal.

  ``` 
  git clone https://github.com/kulisarawiangin/ku-polls.git
  ```
  
2. move to your project directory by type this
  ``` 
  cd ku-polls
  ```
3. create environment
``` 
  python -m venv env
 ```
 4. activate env
 ``` 
  . env/bin/activate  
 ```
5. install requirement by run this command

 ``` 
  pip install -r requirements.txt
 ```
 you can deactivate env by type this command
 ``` 
  deactivate
 ```
 6. Create file name .env to configuration as sample.env in git repository
 7. migrate data and load it
 ``` 
 python manage.py migrate
 python manage.py loaddata data/*.json
 ```
 6. run server by type this command in your terminal.
 ``` 
 python manage.py runserver
 ```
 7. You can use website at 
 ``` 
 localhost:8000/ or http://127.0.0.1:8000/
 ``` 
This web application has two link ```/polls``` and ```/admin``` 
but the main page is ```/polls```.

Admin  provide by initial data
| Username  | Password  |
|-----------|-----------|
|   Kulisara   | P@ssw0rd |

User provide by initial data

| Username  | Password  |
|-----------|-----------|
|   jay   | jay12345 |
|   harry   | harry12345 |

# Project Documents
All project documents are in the [Project Wiki](../../wiki/Home)

* [Vision Statement](../../wiki/Vision-Statement) <br>
* [Requirements](../../wiki/Requirements) <br>
* [Project Plan](../../wiki/Development-Plan) <br>
* [Iteration 1 Plan](../../wiki/Iteration-1-Plan) and [Task Board](https://github.com/users/kulisarawiangin/projects/2/views/2)
* [Iteration 2 Plan](../../wiki/Iteration-2-Plan) and [Task Bord](https://github.com/users/kulisarawiangin/projects/4/views/2)
* [Iteration 3 Plan](../../wiki/Iteration-3-Plan) and [Task Bord](https://github.com/users/kulisarawiangin/projects/5/views/2?layout=board)
* [Iteration 4 Plan](../../wiki/Iteration-4-Plan) and [Task Bord](https://github.com/users/kulisarawiangin/projects/6/views/2?layout=board)
