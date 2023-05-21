## Getting Started
# Home
![Default Home View](./screenshot/bookish.png?raw=true "Title")
# Profile
![Default Home View](./screenshot/profile.png?raw=true "Title")
# Other User Profile
![Default Home View](./screenshot/user.png?raw=true "Title")

Setup project environment with python -m venv myenv.

```bash
$ git clone https://github.com/ikram9820/bookishpdf.git
$ cd bookishpdf
$ python -m venv .venv
# The Activation command is only for windows CMD
$ ./venv/Scripts/Activate.ps1
$ pip install -r requirements.txt

$ python manage.py makemigrations books
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py seed_db
$ python manage.py runserver
```
