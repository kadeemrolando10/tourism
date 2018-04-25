** Python 3 **
version:  3.6.4 or superior

**Create virtual env**

`virtualenv venv
`

_activate env OSX & Linux_

`source venv/bin/activate`


activate env windows 

`cd venv/Scripts/
`

`activate
`

**Install dependencies**

`pip3 install -r requirements.txt`


**Migrate DB**

`python3 manage.py migrate`

**Run Server**

`python3 manage.py runserver`

**others


python3 manage.py startapp reservations

** create requirements.txt

pip freeze > requirements.txt