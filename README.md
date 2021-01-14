[![HitCount](http://hits.dwyl.com/Shinobi3456/Shinobi3456/testFunBox.svg)](http://hits.dwyl.com/Shinobi3456/Shinobi3456/testFunBox)

# Test for developer (Django + Redis)

This repository contains the code for this [test for developer python](https://funbox.ru/q/python.pdf).
Web application for simple accounting of visitors (no matter how, by whom and when)
links.

## Getting Started

- [ ] [Python =>3.8](https://realpython.com/installing-python/)
- [ ] [Pipenv](https://pipenv.readthedocs.io/en/latest/#install-pipenv-today)
- [ ] [Redis](https://redis.io/download)
- [ ] [Git]()
- [ ] An IDE or Editor of your choice

### Running the Application

1. Clone the repository
```
$ git clone https://github.com/Shinobi3456/testFunBox.git
```

2. Check into the cloned repository
```
$ cd testFunBox
```

3. If you are using Pipenv, setup the virtual environment and start it as follows:
```
$ pipenv install && pipenv shell
```

4. Install the requirements
```
$ pip install -r requirements.txt
```

4. Configure Redis configuration in `TestFunBox/settings.py`

5. Start the Django API
```
$ python manage.py runserver
```

6. Run tests
```
$ python manage.py test
```

7. Send requests to post `http://localhost:8000/api/visited_links`

Request data:
```json
{
    "links": [
        "https://ya.ru",
        "https://ya.ru?q=123",
        "https://funbox.ru",
        "https://stackoverflowdsfsdfds.com/questions/11828270/how-to-exit-the-vim-editor"
    ]
}
```

Response Success

```json
{
    "status": "ok"
}
```

Response Error

```json
{
    "status": "error" 
}
```
error - this is the error text